# -*- coding: utf-8 -*-
"""
Performance Optimization Module

Features:
- Parallel image uploads
- Multi-threaded processing
- Memory optimization for large files
- Streaming processing
- Connection pooling
- Caching strategies
- GPU acceleration (optional)
"""

import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable, Any, Dict, Optional
from dataclasses import dataclass
from queue import Queue
import time

from common.logger import get_logger


logger = get_logger(__name__)


@dataclass
class PerformanceConfig:
    """Performance optimization configuration."""
    max_workers: int = 4
    chunk_size_mb: int = 100
    enable_connection_pool: bool = True
    max_connections: int = 10
    use_compression: bool = True
    memory_limit_mb: int = 512
    enable_gpu: bool = False


class ParallelUploader:
    """
    Parallel image uploader for faster processing.
    
    Uploads multiple images simultaneously using thread pool.
    """
    
    def __init__(self, max_workers: int = 4):
        """
        Initialize parallel uploader.
        
        Args:
            max_workers: Maximum number of concurrent uploads
        """
        self.max_workers = max_workers
        self.logger = logger
    
    def upload_images(
        self,
        images: List[bytes],
        upload_function: Callable,
        progress_callback: Optional[Callable] = None
    ) -> List[Dict]:
        """
        Upload multiple images in parallel.
        
        Args:
            images: List of image data
            upload_function: Function to upload single image
            progress_callback: Optional progress callback
            
        Returns:
            List of upload results
        """
        results = []
        completed = 0
        total = len(images)
        
        self.logger.info(f"Starting parallel upload of {total} images with {self.max_workers} workers")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_image = {
                executor.submit(upload_function, img): i 
                for i, img in enumerate(images)
            }
            
            # Process completed tasks
            for future in as_completed(future_to_image):
                img_idx = future_to_image[future]
                
                try:
                    result = future.result()
                    results.append({
                        'index': img_idx,
                        'success': True,
                        'result': result
                    })
                except Exception as e:
                    self.logger.error(f"Image {img_idx} upload failed: {e}")
                    results.append({
                        'index': img_idx,
                        'success': False,
                        'error': str(e)
                    })
                
                completed += 1
                
                if progress_callback:
                    progress_callback(completed, total)
        
        successful = sum(1 for r in results if r['success'])
        self.logger.info(f"Parallel upload completed: {successful}/{total} successful")
        
        return sorted(results, key=lambda x: x['index'])


class StreamProcessor:
    """
    Stream processor for handling large files efficiently.
    
    Processes files in chunks to minimize memory usage.
    """
    
    def __init__(self, chunk_size_mb: int = 100):
        """
        Initialize stream processor.
        
        Args:
            chunk_size_mb: Chunk size in megabytes
        """
        self.chunk_size = chunk_size_mb * 1024 * 1024
        self.logger = logger
    
    def process_large_file(
        self,
        file_path: str,
        process_chunk: Callable[[bytes], Any]
    ) -> List[Any]:
        """
        Process large file in chunks.
        
        Args:
            file_path: Path to file
            process_chunk: Function to process each chunk
            
        Returns:
            List of chunk results
        """
        results = []
        file_size = os.path.getsize(file_path)
        chunks_count = (file_size + self.chunk_size - 1) // self.chunk_size
        
        self.logger.info(f"Processing large file ({file_size / (1024**3):.2f} GB) in {chunks_count} chunks")
        
        with open(file_path, 'rb') as f:
            chunk_num = 0
            while True:
                chunk = f.read(self.chunk_size)
                if not chunk:
                    break
                
                chunk_num += 1
                self.logger.debug(f"Processing chunk {chunk_num}/{chunks_count}")
                
                result = process_chunk(chunk)
                results.append(result)
        
        return results


class ConnectionPool:
    """
    Connection pool for reusing HTTP connections.
    
    Improves performance by avoiding connection overhead.
    """
    
    def __init__(self, max_connections: int = 10):
        """
        Initialize connection pool.
        
        Args:
            max_connections: Maximum number of pooled connections
        """
        self.max_connections = max_connections
        self.pool = Queue(maxsize=max_connections)
        self.lock = threading.Lock()
        self.logger = logger
    
    def get_session(self):
        """
        Get session from pool or create new one.
        
        Returns:
            Requests session
        """
        try:
            return self.pool.get_nowait()
        except:
            import requests
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry
            
            session = requests.Session()
            
            # Configure retries
            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504]
            )
            
            adapter = HTTPAdapter(
                max_retries=retry_strategy,
                pool_connections=self.max_connections,
                pool_maxsize=self.max_connections
            )
            
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            
            return session
    
    def return_session(self, session):
        """
        Return session to pool.
        
        Args:
            session: Session to return
        """
        try:
            self.pool.put_nowait(session)
        except:
            # Pool is full, close session
            session.close()


class MemoryOptimizer:
    """
    Memory optimizer for handling large batches.
    
    Monitors and manages memory usage during processing.
    """
    
    def __init__(self, memory_limit_mb: int = 512):
        """
        Initialize memory optimizer.
        
        Args:
            memory_limit_mb: Memory limit in megabytes
        """
        self.memory_limit = memory_limit_mb * 1024 * 1024
        self.logger = logger
    
    def check_memory(self) -> bool:
        """
        Check if memory usage is within limit.
        
        Returns:
            True if within limit, False otherwise
        """
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            if memory_info.rss > self.memory_limit:
                self.logger.warning(
                    f"Memory usage ({memory_info.rss / (1024**2):.1f} MB) "
                    f"exceeds limit ({self.memory_limit / (1024**2):.1f} MB)"
                )
                return False
            
            return True
        
        except ImportError:
            self.logger.debug("psutil not available, skipping memory check")
            return True
    
    def optimize_batch_size(self, item_size_mb: float, desired_batch: int) -> int:
        """
        Calculate optimal batch size based on memory limit.
        
        Args:
            item_size_mb: Average item size in MB
            desired_batch: Desired batch size
            
        Returns:
            Optimized batch size
        """
        max_batch = int(self.memory_limit / (1024 * 1024) / item_size_mb)
        optimal = min(desired_batch, max_batch)
        
        if optimal < desired_batch:
            self.logger.info(
                f"Reduced batch size from {desired_batch} to {optimal} "
                f"due to memory constraints"
            )
        
        return max(1, optimal)


class PerformanceMonitor:
    """
    Performance monitor for tracking metrics.
    
    Monitors throughput, latency, and resource usage.
    """
    
    def __init__(self):
        """Initialize performance monitor."""
        self.metrics = {
            'operations': 0,
            'total_time': 0.0,
            'total_bytes': 0,
            'errors': 0
        }
        self.lock = threading.Lock()
        self.start_time = time.time()
    
    def record_operation(
        self,
        duration: float,
        bytes_processed: int = 0,
        success: bool = True
    ):
        """
        Record an operation.
        
        Args:
            duration: Operation duration in seconds
            bytes_processed: Number of bytes processed
            success: Whether operation succeeded
        """
        with self.lock:
            self.metrics['operations'] += 1
            self.metrics['total_time'] += duration
            self.metrics['total_bytes'] += bytes_processed
            
            if not success:
                self.metrics['errors'] += 1
    
    def get_stats(self) -> Dict:
        """
        Get performance statistics.
        
        Returns:
            Statistics dictionary
        """
        with self.lock:
            elapsed = time.time() - self.start_time
            
            if self.metrics['operations'] == 0:
                return {
                    'operations': 0,
                    'elapsed_seconds': elapsed,
                    'ops_per_second': 0,
                    'avg_duration': 0,
                    'throughput_mbps': 0,
                    'error_rate': 0
                }
            
            return {
                'operations': self.metrics['operations'],
                'elapsed_seconds': round(elapsed, 2),
                'ops_per_second': round(self.metrics['operations'] / elapsed, 2),
                'avg_duration': round(self.metrics['total_time'] / self.metrics['operations'], 3),
                'throughput_mbps': round(
                    self.metrics['total_bytes'] / (1024 * 1024) / elapsed, 2
                ),
                'error_rate': round(
                    self.metrics['errors'] / self.metrics['operations'] * 100, 2
                ),
                'total_mb': round(self.metrics['total_bytes'] / (1024 * 1024), 2)
            }
    
    def print_stats(self):
        """Print formatted statistics."""
        stats = self.get_stats()
        
        print("\n" + "="*50)
        print("Performance Statistics")
        print("="*50)
        print(f"Operations:     {stats['operations']}")
        print(f"Elapsed:        {stats['elapsed_seconds']}s")
        print(f"Throughput:     {stats['ops_per_second']} ops/s")
        print(f"Avg Duration:   {stats['avg_duration']}s")
        print(f"Data Rate:      {stats['throughput_mbps']} MB/s")
        print(f"Error Rate:     {stats['error_rate']}%")
        print(f"Total Data:     {stats['total_mb']} MB")
        print("="*50 + "\n")


class GPUAccelerator:
    """
    GPU acceleration for image processing (optional).
    
    Uses GPU for image compression and resizing when available.
    """
    
    def __init__(self):
        """Initialize GPU accelerator."""
        self.logger = logger
        self.gpu_available = self._check_gpu()
    
    def _check_gpu(self) -> bool:
        """Check if GPU is available."""
        try:
            import cv2
            count = cv2.cuda.getCudaEnabledDeviceCount()
            
            if count > 0:
                self.logger.info(f"GPU acceleration available ({count} device(s))")
                return True
            else:
                self.logger.info("No CUDA-enabled GPU found")
                return False
        
        except (ImportError, AttributeError):
            self.logger.debug("OpenCV with CUDA support not available")
            return False
    
    def resize_image_gpu(self, image_data: bytes, width: int, height: int) -> bytes:
        """
        Resize image using GPU.
        
        Args:
            image_data: Input image data
            width: Target width
            height: Target height
            
        Returns:
            Resized image data
        """
        if not self.gpu_available:
            raise RuntimeError("GPU not available")
        
        # TODO: Implement GPU-accelerated image resizing
        # This is a placeholder
        self.logger.warning("GPU image resizing not yet implemented")
        return image_data


# Convenience functions
def optimize_parallel_uploads(
    images: List[bytes],
    upload_function: Callable,
    max_workers: int = 4
) -> List[Dict]:
    """
    Optimize image uploads using parallel processing.
    
    Args:
        images: List of images to upload
        upload_function: Upload function
        max_workers: Number of parallel workers
        
    Returns:
        List of results
    """
    uploader = ParallelUploader(max_workers)
    return uploader.upload_images(images, upload_function)


def create_performance_config(
    max_workers: int = 4,
    memory_limit_mb: int = 512,
    enable_gpu: bool = False
) -> PerformanceConfig:
    """
    Create performance configuration.
    
    Args:
        max_workers: Maximum workers
        memory_limit_mb: Memory limit
        enable_gpu: Enable GPU acceleration
        
    Returns:
        PerformanceConfig instance
    """
    return PerformanceConfig(
        max_workers=max_workers,
        memory_limit_mb=memory_limit_mb,
        enable_gpu=enable_gpu
    )
