from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from config.connection import get_db
from database.models import User
from utils.enums import UserRole
from services.authservice import SECRET_KEY, ALGORITHM
from exceptions.custom_exceptions import (
    InvalidTokenException, TokenExpiredException, AuthenticationException,
    UserNotFoundException
)
from config.logging_config import log_error, log_security_event

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            log_security_event("INVALID_TOKEN", details="Missing username in token")
            raise InvalidTokenException()
    except JWTError as e:
        log_security_event("JWT_ERROR", details=f"JWT decode error: {str(e)}")
        raise InvalidTokenException()
        
    user = db.query(User).filter(User.username == username).first()
    
    if user is None:
        log_security_event("USER_NOT_FOUND", username, details="User not found in database")
        raise UserNotFoundException()
        
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

def get_current_instructor(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.INSTRUCTOR:
        log_security_event("UNAUTHORIZED_ACCESS", str(current_user.id), 
                         details=f"User role {current_user.role} attempted instructor access")
        raise AuthenticationException(
            "Access denied. Only instructors can perform this action.",
            current_user.username,
            "insufficient_permissions"
        )
    
    return current_user

def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.ADMIN:
        log_security_event("UNAUTHORIZED_ACCESS", str(current_user.id), 
                         details=f"User role {current_user.role} attempted admin access")
        raise AuthenticationException(
            "Access denied. Only admins can perform this action.",
            current_user.username,
            "insufficient_permissions"
        )
    
    return current_user

def get_current_student(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.STUDENT:
        log_security_event("UNAUTHORIZED_ACCESS", str(current_user.id), 
                         details=f"User role {current_user.role} attempted student access")
        raise AuthenticationException(
            "Access denied. Only students can perform this action.",
            current_user.username,
            "insufficient_permissions"
        )
    
    return current_user