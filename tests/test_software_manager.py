# -*- coding: utf-8 -*-
"""Tests for SoftwareManager."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from unit3dup.media_manager.SoftwareManager import SoftwareManager


class TestSoftwareManager:
    """Test suite for SoftwareManager."""
    
    def test_is_software_file(self):
        """Test software file detection."""
        assert SoftwareManager.is_software_file("app.exe") is True
        assert SoftwareManager.is_software_file("installer.msi") is True
        assert SoftwareManager.is_software_file("program.dmg") is True
        assert SoftwareManager.is_software_file("package.deb") is True
        assert SoftwareManager.is_software_file("video.mp4") is False
        assert SoftwareManager.is_software_file("document.pdf") is False
    
    def test_extract_name(self):
        """Test software name extraction."""
        with patch('pathlib.Path.is_file', return_value=True):
            # Simple case
            sw = SoftwareManager("Adobe_Photoshop_2023.exe")
            assert "Adobe Photoshop" in sw.software_info['name']
            
            # With version
            sw = SoftwareManager("VLC_Media_Player_3.0.18.exe")
            assert "VLC Media Player" in sw.software_info['name']
            
            # With platform
            sw = SoftwareManager("Unity-2022.3.10-Windows.exe")
            assert "Unity" in sw.software_info['name']
    
    def test_extract_version(self):
        """Test version extraction."""
        with patch('pathlib.Path.is_file', return_value=True):
            # Standard version
            sw = SoftwareManager("App_v1.2.3.exe")
            assert sw.software_info['version'] == "1.2.3"
            
            # Year-based version
            sw = SoftwareManager("Software_2023.1.0.exe")
            assert sw.software_info['version'] == "2023.1.0"
            
            # Simple version
            sw = SoftwareManager("Tool_v5.exe")
            assert sw.software_info['version'] == "5"
    
    def test_detect_os(self):
        """Test OS detection."""
        with patch('pathlib.Path.is_file', return_value=True):
            # Windows by extension
            sw = SoftwareManager("app.exe")
            assert sw.software_info['os'] == "windows"
            
            # macOS by extension
            sw = SoftwareManager("installer.dmg")
            assert sw.software_info['os'] == "macos"
            
            # Linux by name
            sw = SoftwareManager("software-linux-x64.tar.gz")
            assert sw.software_info['os'] == "linux"
            
            # Android
            sw = SoftwareManager("app-android.apk")
            assert sw.software_info['os'] == "android"
    
    def test_detect_architecture(self):
        """Test architecture detection."""
        with patch('pathlib.Path.is_file', return_value=True):
            # x64
            sw = SoftwareManager("app-x64.exe")
            assert sw.software_info['architecture'] == "x64"
            
            # x86
            sw = SoftwareManager("installer-x86.msi")
            assert sw.software_info['architecture'] == "x86"
            
            # ARM64
            sw = SoftwareManager("app-arm64.apk")
            assert sw.software_info['architecture'] == "arm64"
            
            # Universal
            sw = SoftwareManager("app-universal.dmg")
            assert sw.software_info['architecture'] == "universal"
    
    def test_extract_edition(self):
        """Test edition extraction."""
        with patch('pathlib.Path.is_file', return_value=True):
            # Pro
            sw = SoftwareManager("Software_Pro_2023.exe")
            assert sw.software_info['edition'] == "Pro"
            
            # Enterprise
            sw = SoftwareManager("App_Enterprise.msi")
            assert sw.software_info['edition'] == "Enterprise"
            
            # Portable
            sw = SoftwareManager("Tool_Portable.exe")
            assert sw.software_info['edition'] == "Portable"
    
    def test_extract_language(self):
        """Test language extraction."""
        with patch('pathlib.Path.is_file', return_value=True):
            # English
            sw = SoftwareManager("App_English.exe")
            assert sw.software_info['language'] == "English"
            
            # Italian
            sw = SoftwareManager("Software_ITA.msi")
            assert sw.software_info['language'] == "Italian"
            
            # Multilingual
            sw = SoftwareManager("Tool_Multilang.exe")
            assert sw.software_info['language'] == "Multilingual"
    
    def test_generate_description(self):
        """Test description generation."""
        with patch('pathlib.Path.is_file', return_value=True):
            with patch('pathlib.Path.stat') as mock_stat:
                mock_stat.return_value.st_size = 1024 * 1024 * 100  # 100 MB
                
                sw = SoftwareManager("Adobe_Photoshop_2023_Pro_Windows_x64.exe")
                description = sw.generate_description()
                
                # Check that description contains key information
                assert "Photoshop" in description or "Adobe" in description
                assert "Version" in description or "2023" in description
                assert "Windows" in description or "windows" in description
                assert "x64" in description
    
    def test_generate_description_with_changelog(self):
        """Test description generation with changelog."""
        with patch('pathlib.Path.is_file', return_value=True):
            with patch('pathlib.Path.stat') as mock_stat:
                mock_stat.return_value.st_size = 1024 * 1024 * 50
                
                sw = SoftwareManager("App_v2.0.exe")
                changelog = "- Added new feature\n- Fixed bug\n- Improved performance"
                description = sw.generate_description(changelog=changelog)
                
                assert "Changelog" in description
                assert "new feature" in description


class TestTrackerTemplate:
    """Test tracker template validation."""
    
    def test_validate_itt_tracker(self):
        """Test that ITT tracker data is valid."""
        from common.trackers.itt import itt_data
        from common.trackers.tracker_template import validate_tracker_data
        
        assert validate_tracker_data(itt_data) is True
    
    def test_validate_sis_tracker(self):
        """Test that SIS tracker data is valid."""
        from common.trackers.sis import sis_data
        from common.trackers.tracker_template import validate_tracker_data
        
        assert validate_tracker_data(sis_data) is True
    
    def test_validate_blutopia_tracker(self):
        """Test that Blutopia tracker data is valid."""
        from common.trackers.blutopia import blutopia_data
        from common.trackers.tracker_template import validate_tracker_data
        
        assert validate_tracker_data(blutopia_data) is True
