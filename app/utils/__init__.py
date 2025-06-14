from .logger import logger, log_error, log_exception

# This makes the logger functions directly importable from app.utils
__all__ = ['logger', 'log_error', 'log_exception']