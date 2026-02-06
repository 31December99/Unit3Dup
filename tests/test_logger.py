# -*- coding: utf-8 -*-
"""Tests for logging module."""

import pytest
import logging
from pathlib import Path
from common.logger import Unit3DupLogger, get_logger, ExitCodes, LogContext


class TestUnit3DupLogger:
    """Test suite for Unit3DupLogger."""
    
    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a logging.Logger instance."""
        logger = Unit3DupLogger.get_logger("test_logger")
        assert isinstance(logger, logging.Logger)
    
    def test_get_logger_singleton(self):
        """Test that same logger name returns same instance."""
        logger1 = Unit3DupLogger.get_logger("test_logger_singleton")
        logger2 = Unit3DupLogger.get_logger("test_logger_singleton")
        assert logger1 is logger2
    
    def test_logger_has_handlers(self):
        """Test that logger has console handler by default."""
        logger = Unit3DupLogger.get_logger("test_logger_handlers")
        assert len(logger.handlers) > 0
    
    def test_convenience_function(self):
        """Test get_logger convenience function."""
        logger = get_logger("test_convenience")
        assert isinstance(logger, logging.Logger)


class TestExitCodes:
    """Test suite for ExitCodes."""
    
    def test_exit_codes_defined(self):
        """Test that exit codes are properly defined."""
        assert ExitCodes.SUCCESS == 0
        assert ExitCodes.GENERAL_ERROR == 1
        assert ExitCodes.CONFIG_ERROR == 2
        assert ExitCodes.CONNECTION_ERROR == 3
        assert ExitCodes.VALIDATION_ERROR == 4
        assert ExitCodes.FILE_NOT_FOUND == 5


class TestLogContext:
    """Test suite for LogContext."""
    
    def test_log_context_success(self):
        """Test LogContext with successful operation."""
        logger = get_logger("test_context_success")
        
        with LogContext("test operation", logger):
            pass  # Successful operation
    
    def test_log_context_with_exception(self):
        """Test LogContext handles exceptions."""
        logger = get_logger("test_context_exception")
        
        # Should not raise, exception is suppressed
        with LogContext("test operation", logger, raise_on_error=False):
            raise ValueError("Test error")
    
    def test_log_context_reraise_exception(self):
        """Test LogContext can re-raise exceptions."""
        logger = get_logger("test_context_reraise")
        
        with pytest.raises(ValueError):
            with LogContext("test operation", logger, raise_on_error=True):
                raise ValueError("Test error")
