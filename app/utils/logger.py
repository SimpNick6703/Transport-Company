import os
import logging
from datetime import datetime
from functools import wraps
import traceback

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Configure logger
logger = logging.getLogger('transport_company')
logger.setLevel(logging.DEBUG)

# Create file handler with automatic daily rotation
log_file = os.path.join(logs_dir, f'transport_{datetime.now().strftime("%Y-%m-%d")}.log')
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.ERROR)  # Only log errors and above to file

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Show all levels in console

# Create formatter and add it to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log_error(func=None, message=None):
    """
    Decorator to log exceptions that occur in functions.
    Can be used with or without parameters.
    
    Examples:
        @log_error
        def function(): pass
        
        @log_error(message="Custom error message")
        def function(): pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Get the error traceback
                error_traceback = traceback.format_exc()
                
                # Log the error with custom message if provided
                log_msg = f"{message or 'Error in'} {func.__name__}: {str(e)}\n{error_traceback}"
                logger.error(log_msg)
                
                # Re-raise the exception to be handled by the caller
                raise
        return wrapper
    
    # Handle case when decorator is used without arguments
    if func is not None:
        return decorator(func)
    return decorator


def log_exception(e, context="", level=logging.ERROR):
    """
    Log an exception that has been caught.
    
    Args:
        e (Exception): The exception to log
        context (str): Additional context about where the exception occurred
        level (int): Logging level (default: ERROR)
    """
    error_traceback = traceback.format_exc()
    log_msg = f"{context}: {str(e)}\n{error_traceback}"
    logger.log(level, log_msg)