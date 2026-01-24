# -*- coding: utf-8 -*-
"""
Centralized configuration manager using Singleton pattern.

This module provides a thread-safe singleton wrapper around the existing
settings.Load class to ensure configuration is loaded once and reused
throughout the application lifecycle.
"""

import threading
from typing import Optional

from common.settings import Load, Config


class ConfigManager:
    """
    Singleton configuration manager.
    
    Ensures that configuration is loaded only once and provides
    thread-safe access to the configuration object throughout
    the application.
    
    Usage:
        config = ConfigManager.get_instance()
        tracker_url = config.tracker_config.ITT_URL
    """
    
    _instance: Optional['ConfigManager'] = None
    _lock: threading.Lock = threading.Lock()
    _config: Optional[Config] = None
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the configuration manager."""
        if self._config is None:
            with self._lock:
                if self._config is None:
                    loader = Load()
                    self._config = loader.load_config()
    
    @classmethod
    def get_instance(cls) -> Config:
        """
        Get the singleton configuration instance.
        
        Returns:
            Config: The application configuration object.
        """
        manager = cls()
        return manager._config
    
    @classmethod
    def reload(cls) -> Config:
        """
        Force reload the configuration from disk.
        
        Useful when configuration file has been modified and
        needs to be reloaded without restarting the application.
        
        Returns:
            Config: The newly loaded configuration object.
        """
        with cls._lock:
            loader = Load()
            cls._instance._config = loader.load_config()
        return cls._instance._config
    
    @property
    def config(self) -> Config:
        """Get the current configuration."""
        return self._config


# Convenience function for quick access
def get_config() -> Config:
    """
    Get the application configuration.
    
    This is a convenience function that returns the singleton
    configuration instance.
    
    Returns:
        Config: The application configuration object.
        
    Example:
        >>> from common.config_manager import get_config
        >>> config = get_config()
        >>> print(config.tracker_config.ITT_URL)
    """
    return ConfigManager.get_instance()
