# -*- coding: utf-8 -*-
"""
Upload Statistics Manager

Tracks upload statistics, success rates, and generates reports.
Provides insights into upload performance and tracker usage.
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict


@dataclass
class UploadRecord:
    """Single upload record."""
    
    timestamp: str
    tracker: str
    category: str
    filename: str
    size_mb: float
    status: str  # success, failed, skipped
    duration_seconds: float
    error_message: Optional[str] = None
    torrent_id: Optional[int] = None


class UploadStatsManager:
    """Manages upload statistics and reporting."""
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize statistics manager.
        
        Args:
            db_path: Path to SQLite database (default: ~/.unit3dup/stats.db)
        """
        if db_path is None:
            db_path = Path.home() / ".unit3dup" / "stats.db"
        
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                tracker TEXT NOT NULL,
                category TEXT NOT NULL,
                filename TEXT NOT NULL,
                size_mb REAL NOT NULL,
                status TEXT NOT NULL,
                duration_seconds REAL NOT NULL,
                error_message TEXT,
                torrent_id INTEGER
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON uploads(timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tracker 
            ON uploads(tracker)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_status 
            ON uploads(status)
        """)
        
        conn.commit()
        conn.close()
    
    def record_upload(self, record: UploadRecord):
        """
        Record an upload attempt.
        
        Args:
            record: UploadRecord instance
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO uploads 
            (timestamp, tracker, category, filename, size_mb, status, 
             duration_seconds, error_message, torrent_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.timestamp,
            record.tracker,
            record.category,
            record.filename,
            record.size_mb,
            record.status,
            record.duration_seconds,
            record.error_message,
            record.torrent_id
        ))
        
        conn.commit()
        conn.close()
    
    def get_stats(self, days: int = 30) -> Dict:
        """
        Get statistics for the last N days.
        
        Args:
            days: Number of days to include
            
        Returns:
            Dictionary with statistics
        """
        since = (datetime.now() - timedelta(days=days)).isoformat()
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Total uploads
        cursor.execute("""
            SELECT COUNT(*) FROM uploads 
            WHERE timestamp >= ?
        """, (since,))
        total_uploads = cursor.fetchone()[0]
        
        # Successful uploads
        cursor.execute("""
            SELECT COUNT(*) FROM uploads 
            WHERE timestamp >= ? AND status = 'success'
        """, (since,))
        successful_uploads = cursor.fetchone()[0]
        
        # Failed uploads
        cursor.execute("""
            SELECT COUNT(*) FROM uploads 
            WHERE timestamp >= ? AND status = 'failed'
        """, (since,))
        failed_uploads = cursor.fetchone()[0]
        
        # Average duration
        cursor.execute("""
            SELECT AVG(duration_seconds) FROM uploads 
            WHERE timestamp >= ? AND status = 'success'
        """, (since,))
        avg_duration = cursor.fetchone()[0] or 0
        
        # Total data uploaded
        cursor.execute("""
            SELECT SUM(size_mb) FROM uploads 
            WHERE timestamp >= ? AND status = 'success'
        """, (since,))
        total_data_mb = cursor.fetchone()[0] or 0
        
        # By tracker
        cursor.execute("""
            SELECT tracker, COUNT(*), 
                   SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful
            FROM uploads 
            WHERE timestamp >= ?
            GROUP BY tracker
            ORDER BY COUNT(*) DESC
        """, (since,))
        by_tracker = [
            {
                'tracker': row[0],
                'total': row[1],
                'successful': row[2],
                'success_rate': (row[2] / row[1] * 100) if row[1] > 0 else 0
            }
            for row in cursor.fetchall()
        ]
        
        # By category
        cursor.execute("""
            SELECT category, COUNT(*) FROM uploads 
            WHERE timestamp >= ?
            GROUP BY category
            ORDER BY COUNT(*) DESC
        """, (since,))
        by_category = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Recent failures
        cursor.execute("""
            SELECT timestamp, tracker, filename, error_message 
            FROM uploads 
            WHERE timestamp >= ? AND status = 'failed'
            ORDER BY timestamp DESC
            LIMIT 10
        """, (since,))
        recent_failures = [
            {
                'timestamp': row[0],
                'tracker': row[1],
                'filename': row[2],
                'error': row[3]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        success_rate = (successful_uploads / total_uploads * 100) if total_uploads > 0 else 0
        
        return {
            'period_days': days,
            'total_uploads': total_uploads,
            'successful_uploads': successful_uploads,
            'failed_uploads': failed_uploads,
            'success_rate': round(success_rate, 2),
            'average_duration_seconds': round(avg_duration, 2),
            'total_data_uploaded_mb': round(total_data_mb, 2),
            'total_data_uploaded_gb': round(total_data_mb / 1024, 2),
            'by_tracker': by_tracker,
            'by_category': by_category,
            'recent_failures': recent_failures
        }
    
    def export_to_json(self, output_path: Path, days: int = 30):
        """
        Export statistics to JSON file.
        
        Args:
            output_path: Output file path
            days: Number of days to include
        """
        stats = self.get_stats(days)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
    
    def export_to_csv(self, output_path: Path, days: int = 30):
        """
        Export raw upload data to CSV.
        
        Args:
            output_path: Output file path
            days: Number of days to include
        """
        import csv
        
        since = (datetime.now() - timedelta(days=days)).isoformat()
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, tracker, category, filename, size_mb, 
                   status, duration_seconds, error_message, torrent_id
            FROM uploads 
            WHERE timestamp >= ?
            ORDER BY timestamp DESC
        """, (since,))
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Timestamp', 'Tracker', 'Category', 'Filename', 'Size (MB)',
                'Status', 'Duration (s)', 'Error', 'Torrent ID'
            ])
            writer.writerows(cursor.fetchall())
        
        conn.close()
    
    def get_upload_history(self, limit: int = 50) -> List[Dict]:
        """
        Get recent upload history.
        
        Args:
            limit: Maximum number of records
            
        Returns:
            List of upload records
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, tracker, category, filename, size_mb, 
                   status, duration_seconds, error_message
            FROM uploads 
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        history = [
            {
                'timestamp': row[0],
                'tracker': row[1],
                'category': row[2],
                'filename': row[3],
                'size_mb': row[4],
                'status': row[5],
                'duration_seconds': row[6],
                'error_message': row[7]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        return history
    
    def clear_old_records(self, days: int = 90):
        """
        Delete records older than N days.
        
        Args:
            days: Keep records from last N days
        """
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM uploads WHERE timestamp < ?
        """, (cutoff,))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted
    
    def print_summary(self, days: int = 7):
        """
        Print formatted statistics summary.
        
        Args:
            days: Number of days to include
        """
        stats = self.get_stats(days)
        
        print(f"\n{'='*60}")
        print(f"Upload Statistics - Last {days} Days")
        print(f"{'='*60}\n")
        
        print(f"Total Uploads:     {stats['total_uploads']}")
        print(f"Successful:        {stats['successful_uploads']} "
              f"({stats['success_rate']}%)")
        print(f"Failed:            {stats['failed_uploads']}")
        print(f"Avg Duration:      {stats['average_duration_seconds']:.1f}s")
        print(f"Total Data:        {stats['total_data_uploaded_gb']:.2f} GB\n")
        
        if stats['by_tracker']:
            print("By Tracker:")
            for tracker_stats in stats['by_tracker']:
                print(f"  {tracker_stats['tracker']}: "
                      f"{tracker_stats['successful']}/{tracker_stats['total']} "
                      f"({tracker_stats['success_rate']:.1f}%)")
        
        if stats['by_category']:
            print("\nBy Category:")
            for category, count in stats['by_category'].items():
                print(f"  {category}: {count}")
        
        if stats['recent_failures']:
            print("\nRecent Failures:")
            for failure in stats['recent_failures'][:5]:
                print(f"  [{failure['timestamp']}] {failure['tracker']}: "
                      f"{failure['filename']}")
                if failure['error']:
                    print(f"    Error: {failure['error']}")
        
        print(f"\n{'='*60}\n")


# Helper function for easy access
def get_stats_manager(db_path: Optional[Path] = None) -> UploadStatsManager:
    """
    Get statistics manager instance.
    
    Args:
        db_path: Optional custom database path
        
    Returns:
        UploadStatsManager instance
    """
    return UploadStatsManager(db_path)
