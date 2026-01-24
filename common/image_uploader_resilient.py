# -*- coding: utf-8 -*-
"""
Resilient Image Uploader with Multi-Host Fallback

Provides robust image uploading with automatic fallback to alternative
hosts when primary host fails. Includes retry logic, queue management,
and comprehensive error handling.
"""

import time
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from enum import Enum
from queue import Queue
from threading import Lock

from common.external_services.imageHost import (
    ImgBB, FreeImage, PtScreens, LensDump, 
    ImgFI, PassIMA, ImaRide
)
from common.logger import get_logger
from common import config_settings


logger = get_logger(__name__)


class UploadStatus(Enum):
    """Upload status enumeration."""
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"
    QUEUED = "queued"


@dataclass
class UploadResult:
    """Result of an image upload attempt."""
    status: UploadStatus
    url: Optional[str] = None
    host: Optional[str] = None
    attempts: int = 0
    error: Optional[str] = None
    duration: float = 0.0


@dataclass
class ImageUploadTask:
    """Image upload task for queue processing."""
    image_data: bytes
    image_name: str
    priority: int = 0  # Higher = more important
    max_retries: int = 3
    current_attempt: int = 0


class ResilientImageUploader:
    """
    Resilient image uploader with multi-host fallback.
    
    Features:
    - Automatic fallback to alternative hosts
    - Retry with exponential backoff
    - Priority-based upload queue
    - Success rate tracking per host
    - Parallel upload support
    """
    
    def __init__(self):
        """Initialize resilient uploader."""
        self.logger = logger
        self.upload_queue = Queue()
        self.lock = Lock()
        
        # Track host performance
        self.host_stats: Dict[str, Dict] = {}
        
        # Initialize available hosts with priorities from config
        self.hosts = self._initialize_hosts()
    
    def _initialize_hosts(self) -> List[Tuple[str, object, int]]:
        """
        Initialize image hosts with priority order.
        
        Returns:
            List of (name, class, priority) tuples
        """
        hosts = []
        
        # Add hosts if keys are configured
        if config_settings.tracker_config.PTSCREENS_KEY:
            hosts.append((
                'PtScreens',
                PtScreens,
                config_settings.user_preferences.PTSCREENS_PRIORITY
            ))
        
        if config_settings.tracker_config.LENSDUMP_KEY:
            hosts.append((
                'LensDump',
                LensDump,
                config_settings.user_preferences.LENSDUMP_PRIORITY
            ))
        
        if config_settings.tracker_config.FREE_IMAGE_KEY:
            hosts.append((
                'FreeImage',
                FreeImage,
                config_settings.user_preferences.FREE_IMAGE_PRIORITY
            ))
        
        if config_settings.tracker_config.IMGBB_KEY:
            hosts.append((
                'ImgBB',
                ImgBB,
                config_settings.user_preferences.IMGBB_PRIORITY
            ))
        
        if config_settings.tracker_config.IMGFI_KEY:
            hosts.append((
                'ImgFI',
                ImgFI,
                config_settings.user_preferences.IMGFI_PRIORITY
            ))
        
        if config_settings.tracker_config.PASSIMA_KEY:
            hosts.append((
                'PassIMA',
                PassIMA,
                config_settings.user_preferences.PASSIMA_PRIORITY
            ))
        
        if config_settings.tracker_config.IMARIDE_KEY:
            hosts.append((
                'ImaRide',
                ImaRide,
                config_settings.user_preferences.IMARIDE_PRIORITY
            ))
        
        # Sort by priority (lower number = higher priority)
        hosts.sort(key=lambda x: x[2])
        
        # Initialize stats for each host
        for name, _, _ in hosts:
            self.host_stats[name] = {
                'attempts': 0,
                'successes': 0,
                'failures': 0,
                'avg_duration': 0.0,
                'last_failure': None
            }
        
        return hosts
    
    def upload_with_fallback(
        self, 
        image_data: bytes, 
        image_name: str,
        max_retries: int = 2
    ) -> UploadResult:
        """
        Upload image with automatic fallback to alternative hosts.
        
        Args:
            image_data: Image data in bytes
            image_name: Name of the image
            max_retries: Maximum retries per host
            
        Returns:
            UploadResult with status and URL
        """
        if not self.hosts:
            return UploadResult(
                status=UploadStatus.FAILED,
                error="No image hosts configured"
            )
        
        # Try each host in priority order
        for host_name, host_class, priority in self.hosts:
            self.logger.info(f"Attempting upload to {host_name} (priority: {priority})")
            
            result = self._upload_to_host(
                host_name,
                host_class,
                image_data,
                image_name,
                max_retries
            )
            
            if result.status == UploadStatus.SUCCESS:
                self.logger.info(f"Successfully uploaded to {host_name}")
                return result
            
            self.logger.warning(
                f"Failed to upload to {host_name}: {result.error}. "
                f"Trying next host..."
            )
        
        # All hosts failed
        return UploadResult(
            status=UploadStatus.FAILED,
            error="All image hosts failed",
            attempts=sum(self.host_stats[h[0]]['attempts'] for h in self.hosts)
        )
    
    def _upload_to_host(
        self,
        host_name: str,
        host_class: type,
        image_data: bytes,
        image_name: str,
        max_retries: int
    ) -> UploadResult:
        """
        Upload to specific host with retry logic.
        
        Args:
            host_name: Name of the host
            host_class: Host class
            image_data: Image data
            image_name: Image name
            max_retries: Maximum retry attempts
            
        Returns:
            UploadResult
        """
        start_time = time.time()
        
        for attempt in range(max_retries):
            try:
                # Update stats
                with self.lock:
                    self.host_stats[host_name]['attempts'] += 1
                
                # Get API key for this host
                api_key = self._get_api_key(host_name)
                if not api_key:
                    return UploadResult(
                        status=UploadStatus.FAILED,
                        host=host_name,
                        error=f"No API key configured for {host_name}"
                    )
                
                # Create uploader instance
                uploader = host_class(
                    image=image_data,
                    key=api_key,
                    image_name=image_name
                )
                
                # Attempt upload
                response = uploader.upload()
                
                if response:
                    # Extract URL from response (format varies by host)
                    url = self._extract_url(response, host_name)
                    
                    if url:
                        duration = time.time() - start_time
                        
                        # Update stats
                        with self.lock:
                            stats = self.host_stats[host_name]
                            stats['successes'] += 1
                            # Update rolling average
                            total_success = stats['successes']
                            stats['avg_duration'] = (
                                (stats['avg_duration'] * (total_success - 1) + duration) 
                                / total_success
                            )
                        
                        return UploadResult(
                            status=UploadStatus.SUCCESS,
                            url=url,
                            host=host_name,
                            attempts=attempt + 1,
                            duration=duration
                        )
                
                # If no URL extracted, it's a failure
                raise Exception("Failed to extract URL from response")
            
            except Exception as e:
                error_msg = str(e)
                self.logger.warning(
                    f"Upload attempt {attempt + 1}/{max_retries} to {host_name} "
                    f"failed: {error_msg}"
                )
                
                # Update failure stats
                with self.lock:
                    self.host_stats[host_name]['failures'] += 1
                    self.host_stats[host_name]['last_failure'] = time.time()
                
                # Exponential backoff before retry
                if attempt < max_retries - 1:
                    backoff = 2 ** attempt  # 1s, 2s, 4s...
                    time.sleep(backoff)
                else:
                    return UploadResult(
                        status=UploadStatus.FAILED,
                        host=host_name,
                        attempts=attempt + 1,
                        error=error_msg
                    )
        
        return UploadResult(
            status=UploadStatus.FAILED,
            host=host_name,
            error="Max retries exceeded"
        )
    
    def _get_api_key(self, host_name: str) -> Optional[str]:
        """Get API key for specified host."""
        key_mapping = {
            'PtScreens': config_settings.tracker_config.PTSCREENS_KEY,
            'LensDump': config_settings.tracker_config.LENSDUMP_KEY,
            'FreeImage': config_settings.tracker_config.FREE_IMAGE_KEY,
            'ImgBB': config_settings.tracker_config.IMGBB_KEY,
            'ImgFI': config_settings.tracker_config.IMGFI_KEY,
            'PassIMA': config_settings.tracker_config.PASSIMA_KEY,
            'ImaRide': config_settings.tracker_config.IMARIDE_KEY,
        }
        return key_mapping.get(host_name)
    
    def _extract_url(self, response: Dict, host_name: str) -> Optional[str]:
        """
        Extract image URL from host response.
        
        Args:
            response: API response
            host_name: Name of the host
            
        Returns:
            Image URL or None
        """
        # Each host has different response format
        try:
            if host_name == 'ImgBB':
                return response.get('data', {}).get('url')
            elif host_name == 'FreeImage':
                return response.get('image', {}).get('url')
            elif host_name in ['PtScreens', 'LensDump', 'ImgFI']:
                return response.get('data', {}).get('image', {}).get('url')
            elif host_name in ['PassIMA', 'ImaRide']:
                return response.get('data', {}).get('url')
            else:
                # Generic extraction
                if 'url' in response:
                    return response['url']
                if 'data' in response and 'url' in response['data']:
                    return response['data']['url']
        except Exception as e:
            self.logger.error(f"Failed to extract URL from {host_name}: {e}")
        
        return None
    
    def get_host_stats(self) -> Dict[str, Dict]:
        """
        Get performance statistics for all hosts.
        
        Returns:
            Dictionary with host statistics
        """
        with self.lock:
            stats = {}
            for host_name, host_stats in self.host_stats.items():
                success_rate = 0.0
                if host_stats['attempts'] > 0:
                    success_rate = (
                        host_stats['successes'] / host_stats['attempts'] * 100
                    )
                
                stats[host_name] = {
                    'attempts': host_stats['attempts'],
                    'successes': host_stats['successes'],
                    'failures': host_stats['failures'],
                    'success_rate': round(success_rate, 2),
                    'avg_duration': round(host_stats['avg_duration'], 2)
                }
            
            return stats
    
    def print_stats(self):
        """Print formatted host statistics."""
        print("\n" + "="*60)
        print("Image Host Performance Statistics")
        print("="*60 + "\n")
        
        stats = self.get_host_stats()
        
        for host, data in stats.items():
            if data['attempts'] > 0:
                print(f"{host}:")
                print(f"  Attempts:     {data['attempts']}")
                print(f"  Successes:    {data['successes']}")
                print(f"  Failures:     {data['failures']}")
                print(f"  Success Rate: {data['success_rate']}%")
                print(f"  Avg Duration: {data['avg_duration']:.2f}s")
                print()
        
        print("="*60 + "\n")


# Convenience function
def upload_image_resilient(
    image_data: bytes,
    image_name: str,
    max_retries: int = 2
) -> UploadResult:
    """
    Upload image with automatic fallback.
    
    Args:
        image_data: Image bytes
        image_name: Image filename
        max_retries: Max retries per host
        
    Returns:
        UploadResult
    """
    uploader = ResilientImageUploader()
    return uploader.upload_with_fallback(image_data, image_name, max_retries)
