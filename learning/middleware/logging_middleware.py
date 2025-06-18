import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from config.logging_config import log_api_request, log_error, log_performance

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Start time for performance measurement
        start_time = time.time()
        
        # Extract request details
        method = request.method
        path = request.url.path
        user_id = None
        
        # Try to get user ID from request headers or query params
        try:
            # Check if there's an authorization header
            auth_header = request.headers.get("authorization")
            if auth_header and auth_header.startswith("Bearer "):
                # In a real implementation, you might decode the token here
                # For now, we'll just note that a token is present
                user_id = "authenticated_user"
        except Exception as e:
            logging.warning(f"Error extracting user info: {e}")
        
        # Log the incoming request
        log_api_request(method, path, user_id)
        
        try:
            # Process the request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log the response
            log_api_request(method, path, user_id, response.status_code, duration)
            
            # Log performance for slow requests (> 1 second)
            if duration > 1.0:
                log_performance(f"{method} {path}", duration, f"Slow request detected")
            
            return response
            
        except Exception as e:
            # Calculate duration even for failed requests
            duration = time.time() - start_time
            
            # Log the error
            log_error(
                "API_REQUEST_FAILED",
                str(e),
                user_id,
                f"Method: {method}, Path: {path}, Duration: {duration:.3f}s"
            )
            
            # Re-raise the exception
            raise 