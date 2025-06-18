import traceback
import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from jose import JWTError
from exceptions.custom_exceptions import (
    ELearningException, DatabaseException, AuthenticationException,
    AuthorizationException, ValidationException, CourseException,
    UserException, EmailException, ConfigurationException
)
from config.logging_config import log_error, log_security_event

logger = logging.getLogger(__name__)

async def handle_elearning_exception(request: Request, exc: ELearningException):
    """Handle custom e-learning exceptions"""
    error_response = {
        "error": {
            "code": exc.error_code or "UNKNOWN_ERROR",
            "message": exc.message,
            "details": exc.details,
            "timestamp": str(request.state.start_time) if hasattr(request.state, 'start_time') else None
        }
    }
    
    # Log the error
    log_error(
        exc.error_code or "UNKNOWN_ERROR",
        exc.message,
        exc.details.get("user_id"),
        f"Details: {exc.details}"
    )
    
    # Determine HTTP status code based on exception type
    if isinstance(exc, AuthenticationException):
        status_code = status.HTTP_401_UNAUTHORIZED
    elif isinstance(exc, AuthorizationException):
        status_code = status.HTTP_403_FORBIDDEN
    elif isinstance(exc, ValidationException):
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(exc, (CourseException, UserException)):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, DatabaseException):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    return JSONResponse(status_code=status_code, content=error_response)

async def handle_validation_error(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    error_details = []
    for error in exc.errors():
        error_details.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    error_response = {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "details": {
                "validation_errors": error_details
            },
            "timestamp": str(request.state.start_time) if hasattr(request.state, 'start_time') else None
        }
    }
    
    log_error("VALIDATION_ERROR", "Request validation failed", None, f"Errors: {error_details}")
    
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=error_response)

async def handle_http_exception(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    error_response = {
        "error": {
            "code": "HTTP_ERROR",
            "message": exc.detail,
            "details": {
                "status_code": exc.status_code
            },
            "timestamp": str(request.state.start_time) if hasattr(request.state, 'start_time') else None
        }
    }
    
    log_error("HTTP_ERROR", exc.detail, None, f"Status: {exc.status_code}")
    
    return JSONResponse(status_code=exc.status_code, content=error_response)

async def handle_database_error(request: Request, exc: SQLAlchemyError):
    """Handle database-related errors"""
    error_message = "Database operation failed"
    error_details = {"operation": "database_operation"}
    
    if isinstance(exc, IntegrityError):
        error_message = "Database integrity constraint violated"
        error_details["constraint"] = str(exc.orig) if exc.orig else "unknown"
    elif isinstance(exc, OperationalError):
        error_message = "Database connection error"
        error_details["connection_error"] = str(exc.orig) if exc.orig else "unknown"
    
    error_response = {
        "error": {
            "code": "DATABASE_ERROR",
            "message": error_message,
            "details": error_details,
            "timestamp": str(request.state.start_time) if hasattr(request.state, 'start_time') else None
        }
    }
    
    log_error("DATABASE_ERROR", error_message, None, f"Details: {error_details}")
    
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_response)

async def handle_jwt_error(request: Request, exc: JWTError):
    """Handle JWT-related errors"""
    error_response = {
        "error": {
            "code": "JWT_ERROR",
            "message": "Invalid or expired token",
            "details": {
                "jwt_error": str(exc)
            },
            "timestamp": str(request.state.start_time) if hasattr(request.state, 'start_time') else None
        }
    }
    
    log_error("JWT_ERROR", "Invalid or expired token", None, f"JWT Error: {str(exc)}")
    log_security_event("INVALID_TOKEN", None, details=f"JWT Error: {str(exc)}")
    
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error_response)

async def handle_generic_exception(request: Request, exc: Exception):
    """Handle all other exceptions"""
    # Get the full traceback for debugging
    tb = traceback.format_exc()
    
    error_response = {
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "details": {
                "exception_type": type(exc).__name__,
                "exception_message": str(exc)
            },
            "timestamp": str(request.state.start_time) if hasattr(request.state, 'start_time') else None
        }
    }
    
    # Log the full error with traceback
    log_error("INTERNAL_SERVER_ERROR", str(exc), None, f"Traceback: {tb}")
    
    # In production, you might want to hide the traceback from the response
    if hasattr(request.app.state, 'debug') and request.app.state.debug:
        error_response["error"]["details"]["traceback"] = tb
    
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_response)

def setup_error_handlers(app):
    """Setup all error handlers for the FastAPI application"""
    
    # Custom e-learning exceptions
    app.add_exception_handler(ELearningException, handle_elearning_exception)
    app.add_exception_handler(DatabaseException, handle_elearning_exception)
    app.add_exception_handler(AuthenticationException, handle_elearning_exception)
    app.add_exception_handler(AuthorizationException, handle_elearning_exception)
    app.add_exception_handler(ValidationException, handle_elearning_exception)
    app.add_exception_handler(CourseException, handle_elearning_exception)
    app.add_exception_handler(UserException, handle_elearning_exception)
    app.add_exception_handler(EmailException, handle_elearning_exception)
    app.add_exception_handler(ConfigurationException, handle_elearning_exception)
    
    # Pydantic validation errors
    app.add_exception_handler(RequestValidationError, handle_validation_error)
    
    # HTTP exceptions
    app.add_exception_handler(StarletteHTTPException, handle_http_exception)
    
    # Database errors
    app.add_exception_handler(SQLAlchemyError, handle_database_error)
    app.add_exception_handler(IntegrityError, handle_database_error)
    app.add_exception_handler(OperationalError, handle_database_error)
    
    # JWT errors
    app.add_exception_handler(JWTError, handle_jwt_error)
    
    # Generic exception handler (should be last)
    app.add_exception_handler(Exception, handle_generic_exception) 