# -*- coding: utf-8 -*-
"""
Enhanced Batch Processing System

Features:
- Progress tracking with detailed status
- Pause/resume capability
- Skip problematic files
- Dry-run mode (preview without upload)
- Batch configuration profiles
- Concurrent processing (optional)
- Automatic error recovery
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import threading

from common.logger import get_logger


logger = get_logger(__name__)


class BatchStatus(Enum):
    """Batch processing status."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ItemStatus(Enum):
    """Individual item status."""
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class BatchItem:
    """Single item in batch."""
    id: str
    path: str
    status: ItemStatus = ItemStatus.PENDING
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    result: Optional[Dict] = None


@dataclass
class BatchConfig:
    """Batch processing configuration."""
    name: str
    dry_run: bool = False
    max_workers: int = 1
    stop_on_error: bool = False
    skip_duplicates: bool = True
    retry_failed: bool = True
    retry_count: int = 2
    retry_delay: float = 5.0
    save_state: bool = True
    state_file: Optional[Path] = None


class BatchProcessor:
    """
    Enhanced batch processor with progress tracking and pause/resume.
    
    Supports:
    - Real-time progress updates
    - Pause and resume operations
    - State persistence
    - Error recovery
    - Dry-run mode
    """
    
    def __init__(
        self,
        config: BatchConfig,
        process_function: Callable,
        items: Optional[List[str]] = None
    ):
        """
        Initialize batch processor.
        
        Args:
            config: Batch configuration
            process_function: Function to process each item
            items: List of item paths to process
        """
        self.config = config
        self.process_function = process_function
        self.logger = logger
        
        self.items: List[BatchItem] = []
        if items:
            self.items = [
                BatchItem(id=str(i), path=item)
                for i, item in enumerate(items)
            ]
        
        self.status = BatchStatus.PENDING
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        
        self._pause_event = threading.Event()
        self._pause_event.set()  # Not paused initially
        self._stop_event = threading.Event()
        
        # Load state if exists
        if config.save_state and config.state_file and config.state_file.exists():
            self._load_state()
    
    def add_item(self, path: str):
        """Add item to batch."""
        item = BatchItem(
            id=str(len(self.items)),
            path=path
        )
        self.items.append(item)
    
    def add_items(self, paths: List[str]):
        """Add multiple items to batch."""
        for path in paths:
            self.add_item(path)
    
    def process(self) -> Dict:
        """
        Process all items in batch.
        
        Returns:
            Summary dictionary
        """
        if self.status == BatchStatus.RUNNING:
            raise RuntimeError("Batch is already running")
        
        self.status = BatchStatus.RUNNING
        self.start_time = time.time()
        
        self.logger.info(
            f"Starting batch '{self.config.name}' with {len(self.items)} items"
            f"{' (DRY RUN)' if self.config.dry_run else ''}"
        )
        
        try:
            if self.config.max_workers > 1:
                self._process_concurrent()
            else:
                self._process_sequential()
            
            self.status = BatchStatus.COMPLETED
        
        except KeyboardInterrupt:
            self.logger.warning("Batch processing cancelled by user")
            self.status = BatchStatus.CANCELLED
        
        except Exception as e:
            self.logger.error(f"Batch processing failed: {e}")
            self.status = BatchStatus.FAILED
        
        finally:
            self.end_time = time.time()
            if self.config.save_state:
                self._save_state()
        
        return self.get_summary()
    
    def _process_sequential(self):
        """Process items sequentially."""
        for item in self.items:
            # Check if should stop
            if self._stop_event.is_set():
                self.logger.info("Stop requested, ending batch")
                break
            
            # Wait if paused
            self._pause_event.wait()
            
            # Skip already processed items
            if item.status in [ItemStatus.SUCCESS, ItemStatus.SKIPPED]:
                continue
            
            self._process_item(item)
            
            # Stop on error if configured
            if (self.config.stop_on_error and 
                item.status == ItemStatus.FAILED):
                self.logger.error("Stopping batch due to error")
                break
    
    def _process_concurrent(self):
        """Process items concurrently (future implementation)."""
        # For now, fall back to sequential
        # TODO: Implement ThreadPoolExecutor for concurrent processing
        self.logger.warning("Concurrent processing not yet implemented, using sequential")
        self._process_sequential()
    
    def _process_item(self, item: BatchItem):
        """
        Process single item.
        
        Args:
            item: BatchItem to process
        """
        item.status = ItemStatus.PROCESSING
        item.start_time = time.time()
        
        self.logger.info(f"Processing [{item.id}]: {Path(item.path).name}")
        
        try:
            if self.config.dry_run:
                # Dry run - simulate processing
                time.sleep(0.1)
                item.result = {"dry_run": True, "path": item.path}
                item.status = ItemStatus.SUCCESS
            else:
                # Actually process
                result = self.process_function(item.path)
                item.result = result
                item.status = ItemStatus.SUCCESS
                self.logger.info(f"Success [{item.id}]: {Path(item.path).name}")
        
        except Exception as e:
            item.error = str(e)
            self.logger.error(f"Failed [{item.id}]: {e}")
            
            # Retry if configured
            if self.config.retry_failed:
                item.status = self._retry_item(item)
            else:
                item.status = ItemStatus.FAILED
        
        finally:
            item.end_time = time.time()
            
            # Save state periodically
            if self.config.save_state:
                self._save_state()
    
    def _retry_item(self, item: BatchItem) -> ItemStatus:
        """
        Retry failed item.
        
        Args:
            item: Item to retry
            
        Returns:
            Final status
        """
        for attempt in range(self.config.retry_count):
            self.logger.info(
                f"Retrying [{item.id}] (attempt {attempt + 1}/{self.config.retry_count})"
            )
            
            time.sleep(self.config.retry_delay)
            
            try:
                result = self.process_function(item.path)
                item.result = result
                item.error = None
                self.logger.info(f"Retry success [{item.id}]")
                return ItemStatus.SUCCESS
            
            except Exception as e:
                item.error = str(e)
                self.logger.warning(f"Retry failed [{item.id}]: {e}")
        
        return ItemStatus.FAILED
    
    def pause(self):
        """Pause batch processing."""
        if self.status == BatchStatus.RUNNING:
            self._pause_event.clear()
            self.status = BatchStatus.PAUSED
            self.logger.info("Batch paused")
    
    def resume(self):
        """Resume batch processing."""
        if self.status == BatchStatus.PAUSED:
            self._pause_event.set()
            self.status = BatchStatus.RUNNING
            self.logger.info("Batch resumed")
    
    def stop(self):
        """Stop batch processing."""
        self._stop_event.set()
        self.resume()  # Unpause if paused
        self.logger.info("Stop requested")
    
    def skip_item(self, item_id: str):
        """
        Skip an item.
        
        Args:
            item_id: ID of item to skip
        """
        for item in self.items:
            if item.id == item_id:
                item.status = ItemStatus.SKIPPED
                self.logger.info(f"Skipped item {item_id}")
                break
    
    def get_progress(self) -> Dict:
        """
        Get current progress.
        
        Returns:
            Progress dictionary
        """
        total = len(self.items)
        processed = sum(
            1 for item in self.items 
            if item.status in [ItemStatus.SUCCESS, ItemStatus.FAILED, ItemStatus.SKIPPED]
        )
        successful = sum(1 for item in self.items if item.status == ItemStatus.SUCCESS)
        failed = sum(1 for item in self.items if item.status == ItemStatus.FAILED)
        skipped = sum(1 for item in self.items if item.status == ItemStatus.SKIPPED)
        
        progress_pct = (processed / total * 100) if total > 0 else 0
        
        elapsed = 0.0
        if self.start_time:
            elapsed = time.time() - self.start_time
        
        eta = 0.0
        if processed > 0 and total > processed:
            avg_time_per_item = elapsed / processed
            eta = avg_time_per_item * (total - processed)
        
        return {
            'total': total,
            'processed': processed,
            'successful': successful,
            'failed': failed,
            'skipped': skipped,
            'progress_percent': round(progress_pct, 1),
            'elapsed_seconds': round(elapsed, 1),
            'eta_seconds': round(eta, 1),
            'status': self.status.value
        }
    
    def get_summary(self) -> Dict:
        """
        Get batch processing summary.
        
        Returns:
            Summary dictionary
        """
        progress = self.get_progress()
        
        duration = 0.0
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
        
        return {
            **progress,
            'batch_name': self.config.name,
            'dry_run': self.config.dry_run,
            'duration_seconds': round(duration, 1),
            'avg_time_per_item': round(
                duration / progress['processed'], 2
            ) if progress['processed'] > 0 else 0,
            'success_rate': round(
                progress['successful'] / progress['total'] * 100, 1
            ) if progress['total'] > 0 else 0
        }
    
    def print_progress(self):
        """Print formatted progress."""
        progress = self.get_progress()
        
        bar_length = 40
        filled = int(bar_length * progress['progress_percent'] / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        print(f"\r[{bar}] {progress['progress_percent']:.1f}% "
              f"({progress['processed']}/{progress['total']}) "
              f"✓{progress['successful']} ✗{progress['failed']} "
              f"⊘{progress['skipped']} "
              f"ETA: {progress['eta_seconds']:.0f}s", end='', flush=True)
    
    def _save_state(self):
        """Save batch state to file."""
        if not self.config.state_file:
            self.config.state_file = Path.home() / ".unit3dup" / f"batch_{self.config.name}.json"
        
        self.config.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        state = {
            'config': asdict(self.config),
            'items': [asdict(item) for item in self.items],
            'status': self.status.value,
            'start_time': self.start_time,
            'end_time': self.end_time
        }
        
        # Convert Path objects to strings
        state['config']['state_file'] = str(state['config']['state_file'])
        
        with open(self.config.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def _load_state(self):
        """Load batch state from file."""
        try:
            with open(self.config.state_file, 'r') as f:
                state = json.load(f)
            
            self.items = [
                BatchItem(
                    id=item['id'],
                    path=item['path'],
                    status=ItemStatus(item['status']),
                    error=item.get('error'),
                    start_time=item.get('start_time'),
                    end_time=item.get('end_time'),
                    result=item.get('result')
                )
                for item in state['items']
            ]
            
            self.status = BatchStatus(state['status'])
            self.start_time = state.get('start_time')
            self.end_time = state.get('end_time')
            
            self.logger.info(f"Loaded batch state from {self.config.state_file}")
        
        except Exception as e:
            self.logger.warning(f"Failed to load batch state: {e}")


# Convenience function
def create_batch_processor(
    name: str,
    items: List[str],
    process_function: Callable,
    dry_run: bool = False,
    **kwargs
) -> BatchProcessor:
    """
    Create batch processor with simple configuration.
    
    Args:
        name: Batch name
        items: List of items to process
        process_function: Processing function
        dry_run: Enable dry-run mode
        **kwargs: Additional config options
        
    Returns:
        BatchProcessor instance
    """
    config = BatchConfig(name=name, dry_run=dry_run, **kwargs)
    return BatchProcessor(config, process_function, items)
