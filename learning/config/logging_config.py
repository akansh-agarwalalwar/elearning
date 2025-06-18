import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Log file paths
auth_log_file = logs_dir / "auth.log"
course_log_file = logs_dir / "courses.log"
user_log_file = logs_dir / "users.log"
error_log_file = logs_dir / "errors.log"
general_log_file = logs_dir / "general.log"

def setup_logger(name: str, log_file: Path, level=logging.INFO):
    """Set up a logger with file and console handlers"""
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create file handler
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create loggers for different components
auth_logger = setup_logger('auth', auth_log_file)
course_logger = setup_logger('courses', course_log_file)
user_logger = setup_logger('users', user_log_file)
error_logger = setup_logger('errors', error_log_file)
general_logger = setup_logger('general', general_log_file)

# Set up root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Create a custom formatter for detailed logging
detailed_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Function to log API requests
def log_api_request(method: str, path: str, user_id: str = None, status_code: int = None, duration: float = None):
    """Log API request details"""
    message = f"API Request: {method} {path}"
    if user_id:
        message += f" | User: {user_id}"
    if status_code:
        message += f" | Status: {status_code}"
    if duration:
        message += f" | Duration: {duration:.3f}s"
    
    general_logger.info(message)

# Function to log authentication events
def log_auth_event(event_type: str, username: str, success: bool, details: str = None):
    """Log authentication events"""
    status = "SUCCESS" if success else "FAILED"
    message = f"AUTH {event_type}: {username} - {status}"
    if details:
        message += f" | Details: {details}"
    
    auth_logger.info(message)

# Function to log course operations
def log_course_operation(operation: str, course_id: str, instructor_id: str, details: str = None):
    """Log course-related operations"""
    message = f"COURSE {operation}: Course ID: {course_id} | Instructor: {instructor_id}"
    if details:
        message += f" | Details: {details}"
    
    course_logger.info(message)

# Function to log user operations
def log_user_operation(operation: str, user_id: str, user_type: str, details: str = None):
    """Log user-related operations"""
    message = f"USER {operation}: User ID: {user_id} | Type: {user_type}"
    if details:
        message += f" | Details: {details}"
    
    user_logger.info(message)

# Function to log errors
def log_error(error_type: str, error_message: str, user_id: str = None, additional_info: str = None):
    """Log error events"""
    message = f"ERROR {error_type}: {error_message}"
    if user_id:
        message += f" | User: {user_id}"
    if additional_info:
        message += f" | Info: {additional_info}"
    
    error_logger.error(message)

# Function to log database operations
def log_db_operation(operation: str, table: str, record_id: str = None, details: str = None):
    """Log database operations"""
    message = f"DB {operation}: Table: {table}"
    if record_id:
        message += f" | Record ID: {record_id}"
    if details:
        message += f" | Details: {details}"
    
    general_logger.info(message)

# Function to log security events
def log_security_event(event_type: str, user_id: str = None, ip_address: str = None, details: str = None):
    """Log security-related events"""
    message = f"SECURITY {event_type}"
    if user_id:
        message += f" | User: {user_id}"
    if ip_address:
        message += f" | IP: {ip_address}"
    if details:
        message += f" | Details: {details}"
    
    auth_logger.warning(message)

# Function to log performance metrics
def log_performance(operation: str, duration: float, additional_info: str = None):
    """Log performance metrics"""
    message = f"PERFORMANCE: {operation} took {duration:.3f}s"
    if additional_info:
        message += f" | {additional_info}"
    
    general_logger.info(message)

# Function to log startup/shutdown events
def log_system_event(event_type: str, details: str = None):
    """Log system startup/shutdown events"""
    message = f"SYSTEM {event_type}"
    if details:
        message += f" | {details}"
    
    general_logger.info(message)

# Export all loggers and functions
__all__ = [
    'auth_logger', 'course_logger', 'user_logger', 'error_logger', 'general_logger',
    'log_api_request', 'log_auth_event', 'log_course_operation', 'log_user_operation',
    'log_error', 'log_db_operation', 'log_security_event', 'log_performance', 'log_system_event'
]