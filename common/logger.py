# -*- coding: utf-8 -*-
"""
Structured logging module for Unit3Dup.

Provides consistent logging across the application with proper
levels, formatting, and error handling.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


class Unit3DupLogger:
    """
    Custom logger for Unit3Dup application.
    
    Provides structured logging with console and optional file output.
    """
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str = "unit3dup", log_file: Optional[Path] = None) -> logging.Logger:
        """
        Get or create a logger instance.
        
        Args:
            name: Logger name
            log_file: Optional path to log file
            
        Returns:
            Configured logger instance
        """
        if name in cls._loggers:
            return cls._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        # Avoid duplicate handlers
        if logger.handlers:
            return logger
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler (optional)
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        cls._loggers[name] = logger
        return logger


class ExitCodes:
    """Standard exit codes for the application."""
    
    SUCCESS = 0
    GENERAL_ERROR = 1
    CONFIG_ERROR = 2
    CONNECTION_ERROR = 3
    VALIDATION_ERROR = 4
    FILE_NOT_FOUND = 5


def safe_exit(message: str, exit_code: int = ExitCodes.GENERAL_ERROR, logger: Optional[logging.Logger] = None) -> None:
    """
    Safely exit the application with proper logging.
    
    Args:
        message: Error message to display
        exit_code: Exit code (default: 1)
        logger: Optional logger instance
    """
    if logger:
        logger.error(message)
    else:
        # Fallback to stderr if no logger provided
        print(f"ERROR: {message}", file=sys.stderr)
    
    sys.exit(exit_code)


class LogContext:
    """Context manager for logging operations with automatic error handling."""
    
    def __init__(self, operation: str, logger: logging.Logger, raise_on_error: bool = False):
        """
        Initialize log context.
        
        Args:
            operation: Description of the operation
            logger: Logger instance
            raise_on_error: Whether to re-raise exceptions
        """
        self.operation = operation
        self.logger = logger
        self.raise_on_error = raise_on_error
        self.start_time = None
    
    def __enter__(self):
        """Enter context."""
        self.start_time = datetime.now()
        self.logger.info(f"Starting: {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context with error handling."""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        if exc_type is None:
            self.logger.info(f"Completed: {self.operation} (took {duration:.2f}s)")
            return True
        
        self.logger.error(
            f"Failed: {self.operation} (after {duration:.2f}s) - {exc_type.__name__}: {exc_val}"
        )
        
        if self.raise_on_error:
            return False  # Re-raise the exception
        
        return True  # Suppress the exception


# Convenience function
def get_logger(name: str = "unit3dup", log_file: Optional[Path] = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name
        log_file: Optional path to log file
        
    Returns:
        Logger instance
        
    Example:
        >>> from common.logger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Starting upload process")
    """
    return Unit3DupLogger.get_logger(name, log_file)
