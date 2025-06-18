
from typing import Optional, Dict, Any

class ELearningException(Exception):
    """Base exception class for e-learning application"""
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class DatabaseException(ELearningException):
    """Database-related exceptions"""
    def __init__(self, message: str, operation: str = None, table: str = None):
        super().__init__(message, "DATABASE_ERROR", {
            "operation": operation,
            "table": table
        })

class AuthenticationException(ELearningException):
    """Authentication-related exceptions"""
    def __init__(self, message: str, username: str = None, reason: str = None):
        super().__init__(message, "AUTHENTICATION_ERROR", {
            "username": username,
            "reason": reason
        })

class AuthorizationException(ELearningException):
    """Authorization-related exceptions"""
    def __init__(self, message: str, user_id: str = None, resource: str = None, action: str = None):
        super().__init__(message, "AUTHORIZATION_ERROR", {
            "user_id": user_id,
            "resource": resource,
            "action": action
        })

class ValidationException(ELearningException):
    """Data validation exceptions"""
    def __init__(self, message: str, field: str = None, value: Any = None):
        super().__init__(message, "VALIDATION_ERROR", {
            "field": field,
            "value": value
        })

class CourseException(ELearningException):
    """Course-related exceptions"""
    def __init__(self, message: str, course_id: str = None, instructor_id: str = None):
        super().__init__(message, "COURSE_ERROR", {
            "course_id": course_id,
            "instructor_id": instructor_id
        })

class UserException(ELearningException):
    """User-related exceptions"""
    def __init__(self, message: str, user_id: str = None, user_type: str = None):
        super().__init__(message, "USER_ERROR", {
            "user_id": user_id,
            "user_type": user_type
        })

class EmailException(ELearningException):
    """Email service exceptions"""
    def __init__(self, message: str, recipient: str = None, email_type: str = None):
        super().__init__(message, "EMAIL_ERROR", {
            "recipient": recipient,
            "email_type": email_type
        })

class ConfigurationException(ELearningException):
    """Configuration-related exceptions"""
    def __init__(self, message: str, config_key: str = None):
        super().__init__(message, "CONFIGURATION_ERROR", {
            "config_key": config_key
        })

# Specific exception classes
class UserAlreadyExistsException(ValidationException):
    """Raised when trying to create a user that already exists"""
    def __init__(self, username: str = None, email: str = None):
        message = "User already exists"
        if username:
            message += f" with username: {username}"
        if email:
            message += f" with email: {email}"
        super().__init__(message, "username" if username else "email", username or email)

class InvalidCredentialsException(AuthenticationException):
    """Raised when login credentials are invalid"""
    def __init__(self, username: str = None):
        super().__init__("Invalid username or password", username, "invalid_credentials")

class TokenExpiredException(AuthenticationException):
    """Raised when JWT token has expired"""
    def __init__(self):
        super().__init__("Token has expired", reason="token_expired")

class InvalidTokenException(AuthenticationException):
    """Raised when JWT token is invalid"""
    def __init__(self):
        super().__init__("Invalid token", reason="invalid_token")

class CourseNotFoundException(CourseException):
    """Raised when course is not found"""
    def __init__(self, course_id: str):
        super().__init__(f"Course not found with ID: {course_id}", course_id)

class CourseAccessDeniedException(AuthorizationException):
    """Raised when user doesn't have permission to access course"""
    def __init__(self, course_id: str, user_id: str):
        super().__init__(
            f"Access denied to course: {course_id}",
            user_id,
            f"course:{course_id}",
            "access"
        )

class UserNotFoundException(UserException):
    """Raised when user is not found"""
    def __init__(self, user_id: str = None, email: str = None):
        identifier = user_id or email
        super().__init__(f"User not found: {identifier}", user_id)

class InvalidUserTypeException(ValidationException):
    """Raised when user type is invalid"""
    def __init__(self, user_type: str):
        super().__init__(f"Invalid user type: {user_type}", "user_type", user_type)

class DatabaseConnectionException(DatabaseException):
    """Raised when database connection fails"""
    def __init__(self, operation: str = None):
        super().__init__("Database connection failed", operation)

class EmailSendException(EmailException):
    """Raised when email sending fails"""
    def __init__(self, recipient: str, email_type: str):
        super().__init__(f"Failed to send {email_type} email to {recipient}", recipient, email_type) 

