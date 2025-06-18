import re
from typing import Dict, Any, List
from email_validator import validate_email, EmailNotValidError
from exceptions.custom_exceptions import (
    ValidationException, DatabaseException
)

def validate_email_format(email: str) -> bool:
    """Validate email format"""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def validate_password_strength(password: str) -> Dict[str, Any]:
    """Validate password strength and return detailed feedback"""
    errors = []
    warnings = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    elif len(password) < 12:
        warnings.append("Consider using a longer password (12+ characters)")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one digit")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        warnings.append("Consider adding special characters for better security")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "strength": "weak" if len(errors) > 0 else "medium" if len(warnings) > 0 else "strong"
    }

def validate_username(username: str) -> Dict[str, Any]:
    """Validate username format and requirements"""
    errors = []
    
    if len(username) < 3:
        errors.append("Username must be at least 3 characters long")
    
    if len(username) > 50:
        errors.append("Username must be no more than 50 characters long")
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        errors.append("Username can only contain letters, numbers, and underscores")
    
    if username.startswith('_') or username.endswith('_'):
        errors.append("Username cannot start or end with underscore")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }

def validate_user_type(user_type: str) -> bool:
    """Validate user type"""
    valid_types = ["student", "instructor", "admin"]
    return user_type.lower() in valid_types

def validate_course_data(title: str, description: str) -> Dict[str, Any]:
    """Validate course data"""
    errors = []
    
    if not title or len(title.strip()) == 0:
        errors.append("Course title is required")
    elif len(title) > 255:
        errors.append("Course title must be no more than 255 characters")
    
    if not description or len(description.strip()) == 0:
        errors.append("Course description is required")
    elif len(description) > 1000:
        errors.append("Course description must be no more than 1000 characters")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }

def sanitize_input(text: str, max_length: int = 1000) -> str:
    """Sanitize user input to prevent injection attacks"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', text)
    
    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized.strip()

def validate_uuid(uuid_string: str) -> bool:
    """Validate UUID format"""
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    return bool(uuid_pattern.match(uuid_string))

def handle_database_operation(operation: str, table: str, error: Exception) -> None:
    """Handle database operation errors"""
    error_message = f"Database operation '{operation}' failed on table '{table}'"
    raise DatabaseException(error_message, operation, table)

def validate_pagination_params(page: int, size: int, max_size: int = 100) -> Dict[str, Any]:
    """Validate pagination parameters"""
    errors = []
    
    if page < 1:
        errors.append("Page number must be greater than 0")
    
    if size < 1:
        errors.append("Page size must be greater than 0")
    elif size > max_size:
        errors.append(f"Page size cannot exceed {max_size}")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "page": max(1, page),
        "size": min(max_size, max(1, size))
    }

def validate_search_query(query: str, min_length: int = 2, max_length: int = 100) -> Dict[str, Any]:
    """Validate search query parameters"""
    errors = []
    
    if not query or len(query.strip()) == 0:
        errors.append("Search query is required")
    elif len(query.strip()) < min_length:
        errors.append(f"Search query must be at least {min_length} characters")
    elif len(query) > max_length:
        errors.append(f"Search query must be no more than {max_length} characters")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "query": query.strip() if query else ""
    }

def format_error_response(error_code: str, message: str, details: Dict[str, Any] = None) -> Dict[str, Any]:
    """Format error response consistently"""
    return {
        "error": {
            "code": error_code,
            "message": message,
            "details": details or {}
        }
    }

def validate_file_upload(filename: str, allowed_extensions: List[str], max_size_mb: int = 10) -> Dict[str, Any]:
    """Validate file upload parameters"""
    errors = []
    
    if not filename:
        errors.append("Filename is required")
    else:
        # Check file extension
        file_extension = filename.lower().split('.')[-1] if '.' in filename else ''
        if file_extension not in allowed_extensions:
            errors.append(f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "extension": file_extension if filename and '.' in filename else None
    }

def validate_date_range(start_date: str, end_date: str) -> Dict[str, Any]:
    """Validate date range parameters"""
    errors = []
    
    try:
        from datetime import datetime
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        if start >= end:
            errors.append("Start date must be before end date")
        
    except ValueError:
        errors.append("Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }

def create_validation_error(field: str, message: str, value: Any = None) -> ValidationException:
    """Create a validation exception with consistent formatting"""
    return ValidationException(message, field, value)

def handle_async_operation_error(operation: str, error: Exception) -> None:
    """Handle errors in async operations"""
    error_message = f"Async operation '{operation}' failed: {str(error)}"
    raise DatabaseException(error_message, operation)

