# -*- coding: utf-8 -*-
"""Tests for CLI command handlers."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from unit3dup.cli_commands import CLICommands, validate_torrent_client


class TestCLICommands:
    """Test suite for CLICommands."""
    
    @patch('unit3dup.cli_commands.get_config')
    def test_cli_commands_initialization(self, mock_get_config):
        """Test CLICommands initialization."""
        mock_config = Mock()
        mock_get_config.return_value = mock_config
        
        cli_args = Mock()
        tracker_list = ["ITT"]
        archive = "/path/to/archive"
        
        cmd = CLICommands(cli_args, tracker_list, archive)
        
        assert cmd.cli_args is cli_args
        assert cmd.tracker_name_list == tracker_list
        assert cmd.tracker_archive == archive
        assert cmd.config is mock_config
    
    @patch('unit3dup.cli_commands.Bot')
    @patch('unit3dup.cli_commands.get_config')
    def test_execute_upload_command(self, mock_get_config, mock_bot):
        """Test execute_upload_command."""
        mock_config = Mock()
        mock_get_config.return_value = mock_config
        
        cli_args = Mock()
        cli_args.upload = "/path/to/file"
        
        cmd = CLICommands(cli_args, ["ITT"], "/archive")
        cmd.execute_upload_command()
        
        # Verify Bot was instantiated and run was called
        mock_bot.assert_called_once()
        mock_bot.return_value.run.assert_called_once()


class TestValidateTorrentClient:
    """Test suite for validate_torrent_client."""
    
    @patch('unit3dup.cli_commands.QbittorrentClient')
    def test_validate_qbittorrent_success(self, mock_client):
        """Test successful qBittorrent validation."""
        mock_config = Mock()
        mock_config.torrent_client_config.TORRENT_CLIENT = "qbittorrent"
        
        mock_instance = Mock()
        mock_instance.connect.return_value = True
        mock_client.return_value = mock_instance
        
        result = validate_torrent_client(mock_config)
        assert result is True
    
    @patch('unit3dup.cli_commands.QbittorrentClient')
    def test_validate_qbittorrent_failure(self, mock_client):
        """Test failed qBittorrent validation."""
        mock_config = Mock()
        mock_config.torrent_client_config.TORRENT_CLIENT = "qbittorrent"
        
        mock_instance = Mock()
        mock_instance.connect.return_value = False
        mock_client.return_value = mock_instance
        
        result = validate_torrent_client(mock_config)
        assert result is False
    
    def test_validate_unknown_client(self):
        """Test validation with unknown client."""
        mock_config = Mock()
        mock_config.torrent_client_config.TORRENT_CLIENT = "unknown_client"
        
        result = validate_torrent_client(mock_config)
        assert result is False
