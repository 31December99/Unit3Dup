# -*- coding: utf-8 -*-
"""Tests for UploadStatsManager."""

import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock
import tempfile

from common.upload_stats import (
    UploadStatsManager, UploadRecord, get_stats_manager
)


class TestUploadStatsManager:
    """Test suite for UploadStatsManager."""
    
    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing."""
        temp_dir = tempfile.mkdtemp()
        db_path = Path(temp_dir) / "test_stats.db"
        yield db_path
        # Cleanup
        if db_path.exists():
            db_path.unlink()
    
    def test_init_creates_database(self, temp_db):
        """Test that initialization creates database."""
        manager = UploadStatsManager(temp_db)
        assert temp_db.exists()
    
    def test_record_upload_success(self, temp_db):
        """Test recording successful upload."""
        manager = UploadStatsManager(temp_db)
        
        record = UploadRecord(
            timestamp=datetime.now().isoformat(),
            tracker="ITT",
            category="movie",
            filename="test.mkv",
            size_mb=1024.5,
            status="success",
            duration_seconds=45.3,
            torrent_id=12345
        )
        
        manager.record_upload(record)
        
        # Verify it was recorded
        stats = manager.get_stats(days=1)
        assert stats['total_uploads'] == 1
        assert stats['successful_uploads'] == 1
    
    def test_record_upload_failure(self, temp_db):
        """Test recording failed upload."""
        manager = UploadStatsManager(temp_db)
        
        record = UploadRecord(
            timestamp=datetime.now().isoformat(),
            tracker="ITT",
            category="tv",
            filename="test.mkv",
            size_mb=512.0,
            status="failed",
            duration_seconds=10.0,
            error_message="Connection timeout"
        )
        
        manager.record_upload(record)
        
        stats = manager.get_stats(days=1)
        assert stats['total_uploads'] == 1
        assert stats['failed_uploads'] == 1
        assert stats['success_rate'] == 0.0
    
    def test_get_stats_calculations(self, temp_db):
        """Test statistics calculations."""
        manager = UploadStatsManager(temp_db)
        
        # Record multiple uploads
        for i in range(5):
            record = UploadRecord(
                timestamp=datetime.now().isoformat(),
                tracker="ITT",
                category="movie",
                filename=f"test{i}.mkv",
                size_mb=1000.0,
                status="success" if i < 4 else "failed",
                duration_seconds=30.0
            )
            manager.record_upload(record)
        
        stats = manager.get_stats(days=1)
        
        assert stats['total_uploads'] == 5
        assert stats['successful_uploads'] == 4
        assert stats['failed_uploads'] == 1
        assert stats['success_rate'] == 80.0
        assert stats['total_data_uploaded_mb'] == 4000.0
    
    def test_stats_by_tracker(self, temp_db):
        """Test statistics grouped by tracker."""
        manager = UploadStatsManager(temp_db)
        
        # Record uploads to different trackers
        for tracker in ["ITT", "SIS", "ITT"]:
            record = UploadRecord(
                timestamp=datetime.now().isoformat(),
                tracker=tracker,
                category="movie",
                filename="test.mkv",
                size_mb=100.0,
                status="success",
                duration_seconds=20.0
            )
            manager.record_upload(record)
        
        stats = manager.get_stats(days=1)
        
        assert len(stats['by_tracker']) == 2
        itt_stats = next(t for t in stats['by_tracker'] if t['tracker'] == 'ITT')
        assert itt_stats['total'] == 2
    
    def test_export_to_json(self, temp_db):
        """Test JSON export."""
        manager = UploadStatsManager(temp_db)
        
        record = UploadRecord(
            timestamp=datetime.now().isoformat(),
            tracker="ITT",
            category="movie",
            filename="test.mkv",
            size_mb=500.0,
            status="success",
            duration_seconds=25.0
        )
        manager.record_upload(record)
        
        output_path = temp_db.parent / "stats.json"
        manager.export_to_json(output_path, days=1)
        
        assert output_path.exists()
        
        # Cleanup
        output_path.unlink()
    
    def test_clear_old_records(self, temp_db):
        """Test clearing old records."""
        manager = UploadStatsManager(temp_db)
        
        # This would need proper date manipulation
        # For now, just test the method exists and runs
        deleted = manager.clear_old_records(days=90)
        assert isinstance(deleted, int)
    
    def test_convenience_function(self, temp_db):
        """Test get_stats_manager convenience function."""
        manager = get_stats_manager(temp_db)
        assert isinstance(manager, UploadStatsManager)


class TestUploadRecord:
    """Test UploadRecord dataclass."""
    
    def test_create_record(self):
        """Test creating upload record."""
        record = UploadRecord(
            timestamp="2024-01-01T12:00:00",
            tracker="ITT",
            category="movie",
            filename="test.mkv",
            size_mb=1024.0,
            status="success",
            duration_seconds=30.5
        )
        
        assert record.tracker == "ITT"
        assert record.status == "success"
        assert record.error_message is None
