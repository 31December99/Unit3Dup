# -*- coding: utf-8 -*-
"""Tests for ConfigManager singleton."""

import pytest
from unittest.mock import Mock, patch
from common.config_manager import ConfigManager, get_config


class TestConfigManager:
    """Test suite for ConfigManager."""
    
    def test_singleton_instance(self):
        """Test that ConfigManager returns the same instance."""
        instance1 = ConfigManager()
        instance2 = ConfigManager()
        assert instance1 is instance2
    
    @patch('common.config_manager.Load')
    def test_config_loaded_once(self, mock_load):
        """Test that configuration is loaded only once."""
        mock_loader = Mock()
        mock_config = Mock()
        mock_loader.load_config.return_value = mock_config
        mock_load.return_value = mock_loader
        
        # Reset singleton for test
        ConfigManager._instance = None
        ConfigManager._config = None
        
        # Create multiple instances
        config1 = ConfigManager.get_instance()
        config2 = ConfigManager.get_instance()
        
        # load_config should be called only once
        assert mock_loader.load_config.call_count == 1
        assert config1 is config2
    
    def test_get_config_convenience_function(self):
        """Test the convenience get_config function."""
        config1 = get_config()
        config2 = get_config()
        assert config1 is config2
