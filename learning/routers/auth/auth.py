from fastapi import APIRouter, HTTPException, status, Depends, Query, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config.connection import get_db
from database.models import User
from utils.enums import UserRole
from services.authservice import hash_password, verify_password, create_access_token
from services.privilege_service import PrivilegeService
from datetime import timedelta
from middleware.auth import get_current_user
from pydantic import BaseModel
from services.emailservice import send_welcome_email
from config.logging_config import (
    log_auth_event, log_user_operation, log_error, log_db_operation,
    log_security_event, log_performance
)
from exceptions.custom_exceptions import (
    UserAlreadyExistsException, InvalidCredentialsException, UserNotFoundException,
    InvalidUserTypeException, DatabaseException, EmailException, ValidationException
)
from utils.error_utils import (
    validate_email_format, validate_password_strength, validate_username,
    validate_user_type, sanitize_input
)
import time

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: str
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreateRequest, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    start_time = time.time()
    
    try:
        # Validate input data
        username_validation = validate_username(user_in.username)
        if not username_validation["is_valid"]:
            raise ValidationException(
                "Username validation failed",
                "username",
                user_in.username
            )
        
        if not validate_email_format(user_in.email):
            raise ValidationException(
                "Invalid email format",
                "email",
                user_in.email
            )
        
        password_validation = validate_password_strength(user_in.password)
        if not password_validation["is_valid"]:
            raise ValidationException(
                "Password does not meet strength requirements",
                "password",
                "***"
            )
        
        # Validate role
        try:
            role = UserRole(user_in.role.lower())
        except ValueError:
            raise InvalidUserTypeException(user_in.role)
        
        # Sanitize inputs
        sanitized_username = sanitize_input(user_in.username, 50)
        sanitized_email = sanitize_input(user_in.email, 100)
        
        # Check if username or email already exists
        existing = db.query(User).filter(
            (User.username == sanitized_username) | (User.email == sanitized_email)
        ).first()
        
        if existing:
            if existing.username == sanitized_username:
                raise UserAlreadyExistsException(username=sanitized_username)
            else:
                raise UserAlreadyExistsException(email=sanitized_email)

        hashed_password = hash_password(user_in.password)
        
        # Create user
        new_user = User(
            username=sanitized_username,
            password=hashed_password,
            email=sanitized_email,
            role=role
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        log_db_operation("CREATE", "users", str(new_user.id), f"Role: {role.value}")
        
        # Assign default privileges if instructor
        if role == UserRole.INSTRUCTOR:
            privilege_service = PrivilegeService(db)
            # Get first admin user for assigning privileges
            admin_user = db.query(User).filter(User.role == UserRole.ADMIN).first()
            if admin_user:
                privilege_service.assign_default_privileges_to_instructor(
                    instructor_id=new_user.id,
                    admin_id=admin_user.id
                )
        
        # Send welcome email in background
        try:
            background_tasks.add_task(send_welcome_email, new_user.email, new_user.username)
        except Exception as e:
            log_error("EMAIL_SEND_FAILED", f"Failed to send welcome email: {str(e)}", str(new_user.id))
            # Don't fail registration if email fails
        
        duration = time.time() - start_time
        log_performance("user_registration", duration, f"Role: {role.value}")
        
        log_auth_event("REGISTER", user_in.username, True, f"Role: {role.value}")
        log_user_operation("CREATE", str(new_user.id), role.value, f"Email: {user_in.email}")
        
        return new_user
        
    except (UserAlreadyExistsException, InvalidUserTypeException, ValidationException):
        raise
    except Exception as e:
        duration = time.time() - start_time
        log_error("REGISTRATION_FAILED", str(e), user_in.username, f"Duration: {duration:.3f}s")
        raise DatabaseException("User registration failed", "CREATE", "users")

@router.post("/login")
async def login(
    login_data: LoginRequest, 
    db: Session = Depends(get_db)
):
    start_time = time.time()
    
    try:
        # Validate input
        if not login_data.username or not login_data.password:
            raise ValidationException("Username and password are required")
        
        # Sanitize username
        sanitized_username = sanitize_input(login_data.username, 50)
        
        # Find user by username
        user = db.query(User).filter(User.username == sanitized_username).first()
        
        if not user or not verify_password(login_data.password, user.password):
            log_auth_event("LOGIN", sanitized_username, False, "Invalid credentials")
            log_security_event("FAILED_LOGIN", sanitized_username, details="Invalid username or password")
            raise InvalidCredentialsException(sanitized_username)
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user.username, "role": user.role.value},
            expires_delta=timedelta(minutes=30)
        )
        
        duration = time.time() - start_time
        log_performance("user_login", duration, f"Role: {user.role.value}")
        
        log_auth_event("LOGIN", user.username, True, f"Role: {user.role.value}")
        log_user_operation("LOGIN", str(user.id), user.role.value)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": user.role.value,
            "username": user.username
        }
        
    except (InvalidCredentialsException, ValidationException):
        raise
    except Exception as e:
        duration = time.time() - start_time
        log_error("LOGIN_FAILED", str(e), login_data.username, f"Duration: {duration:.3f}s")
        raise DatabaseException("Login operation failed", "READ", "users")

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    try:
        log_user_operation("PROFILE_ACCESS", str(current_user.id), current_user.role.value)
        return current_user
    except Exception as e:
        log_error("PROFILE_ACCESS_FAILED", str(e), str(current_user.id))
        raise DatabaseException("Failed to retrieve user profile", "READ", "users")

@router.get("/users", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        log_error("GET_USERS_FAILED", str(e))
        raise DatabaseException("Failed to retrieve users", "READ", "users")

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int, 
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFoundException(str(user_id))
        
        db.delete(user)
        db.commit()
        
        log_user_operation("DELETE", str(user_id), user.role.value)
        return {"message": "User deleted successfully"}
        
    except UserNotFoundException:
        raise
    except Exception as e:
        log_error("DELETE_USER_FAILED", str(e), str(user_id))
        raise DatabaseException("Failed to delete user", "DELETE", "users")
