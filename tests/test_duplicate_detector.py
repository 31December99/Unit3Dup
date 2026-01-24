# -*- coding: utf-8 -*-
"""Tests for EnhancedDuplicateDetector."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile

from common.duplicate_detector import (
    EnhancedDuplicateDetector,
    DuplicateMatch,
    DuplicateType,
    QualityComparison,
    check_for_duplicates
)


class TestEnhancedDuplicateDetector:
    """Test suite for EnhancedDuplicateDetector."""
    
    @pytest.fixture
    def temp_cache(self):
        """Create temporary cache file."""
        temp_dir = tempfile.mkdtemp()
        cache_path = Path(temp_dir) / "hash_cache.json"
        yield cache_path
        if cache_path.exists():
            cache_path.unlink()
    
    def test_init_creates_cache(self, temp_cache):
        """Test initialization creates cache file."""
        detector = EnhancedDuplicateDetector(temp_cache)
        assert detector.hash_cache_path == temp_cache
    
    @patch('pathlib.Path.stat')
    def test_calculate_file_hash(self, mock_stat, temp_cache):
        """Test file hash calculation."""
        detector = EnhancedDuplicateDetector(temp_cache)
        
        # Create a mock file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test content")
            tmp_path = Path(tmp.name)
        
        try:
            file_hash = detector.calculate_file_hash(tmp_path, algorithm='md5')
            assert isinstance(file_hash, str)
            assert len(file_hash) == 32  # MD5 hex length
            
            # Test caching
            cached_hash = detector.calculate_file_hash(tmp_path, algorithm='md5')
            assert cached_hash == file_hash
        finally:
            tmp_path.unlink()
    
    def test_check_duplicate_no_matches(self, temp_cache):
        """Test duplicate check with no matches."""
        detector = EnhancedDuplicateDetector(temp_cache)
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test content")
            tmp_path = Path(tmp.name)
        
        try:
            matches = detector.check_duplicate(
                tmp_path,
                "Test Movie",
                [],
                check_hash=False,
                check_mediainfo=False
            )
            
            assert matches == []
        finally:
            tmp_path.unlink()
    
    def test_should_skip_upload_no_matches(self, temp_cache):
        """Test skip decision with no matches."""
        detector = EnhancedDuplicateDetector(temp_cache)
        
        should_skip, reason = detector.should_skip_upload([])
        assert should_skip is False
        assert reason is None
    
    def test_should_skip_upload_exact_match(self, temp_cache):
        """Test skip decision with exact match."""
        detector = EnhancedDuplicateDetector(temp_cache)
        
        match = DuplicateMatch(
            match_type=DuplicateType.EXACT_HASH,
            confidence=1.0,
            existing_file="existing.mkv"
        )
        
        should_skip, reason = detector.should_skip_upload([match])
        assert should_skip is True
        assert "Exact duplicate" in reason
    
    def test_should_skip_upload_allow_upgrade(self, temp_cache):
        """Test skip decision allowing quality upgrades."""
        detector = EnhancedDuplicateDetector(temp_cache)
        
        match = DuplicateMatch(
            match_type=DuplicateType.TITLE_FUZZY,
            confidence=0.95,
            existing_file="existing.mkv",
            quality_comparison=QualityComparison.BETTER
        )
        
        should_skip, reason = detector.should_skip_upload([match], allow_upgrades=True)
        assert should_skip is False
        assert "upgrade" in reason.lower()
    
    def test_format_matches_empty(self, temp_cache):
        """Test formatting with no matches."""
        detector = EnhancedDuplicateDetector(temp_cache)
        
        output = detector.format_matches([])
        assert "No duplicates" in output
    
    def test_format_matches_with_data(self, temp_cache):
        """Test formatting with matches."""
        detector = EnhancedDuplicateDetector(temp_cache)
        
        match = DuplicateMatch(
            match_type=DuplicateType.EXACT_SIZE,
            confidence=0.95,
            existing_file="test.mkv",
            existing_tracker="ITT",
            details={'title_similarity': 96}
        )
        
        output = detector.format_matches([match])
        assert "exact_size" in output
        assert "95%" in output
        assert "test.mkv" in output
    
    def test_compare_quality_better(self, temp_cache):
        """Test quality comparison (better)."""
        detector = EnhancedDuplicateDetector(temp_cache)
        
        with patch('common.duplicate_detector.MediaFile') as mock_media:
            mock_instance = Mock()
            mock_instance.resolution = "1080p"
            mock_instance.video_codec = "h265"
            mock_media.return_value = mock_instance
            
            result = detector._compare_quality(
                Path("test.mkv"),
                "720p",
                "h264"
            )
            
            assert result == QualityComparison.BETTER
    
    def test_convenience_function(self, temp_cache):
        """Test check_for_duplicates convenience function."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test")
            tmp_path = Path(tmp.name)
        
        try:
            matches = check_for_duplicates(
                tmp_path,
                "Test",
                []
            )
            assert isinstance(matches, list)
        finally:
            tmp_path.unlink()


class TestDuplicateMatch:
    """Test DuplicateMatch dataclass."""
    
    def test_create_match(self):
        """Test creating duplicate match."""
        match = DuplicateMatch(
            match_type=DuplicateType.EXACT_HASH,
            confidence=1.0,
            existing_file="test.mkv",
            existing_tracker="ITT"
        )
        
        assert match.match_type == DuplicateType.EXACT_HASH
        assert match.confidence == 1.0
        assert match.existing_tracker == "ITT"
