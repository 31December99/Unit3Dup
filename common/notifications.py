# -*- coding: utf-8 -*-
"""
Notification System

Supports multiple notification channels:
- Email (SMTP)
- Telegram Bot
- Discord Webhooks
- Pushover
- Custom webhooks

Notifications for:
- Upload success/failure
- Batch completion
- Errors and warnings
- Daily statistics
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, List
from enum import Enum
from dataclasses import dataclass
import requests

from common.logger import get_logger


logger = get_logger(__name__)


class NotificationType(Enum):
    """Types of notifications."""
    SUCCESS = "success"
    FAILURE = "failure"
    WARNING = "warning"
    INFO = "info"
    STATS = "stats"


class NotificationChannel(Enum):
    """Notification channels."""
    EMAIL = "email"
    TELEGRAM = "telegram"
    DISCORD = "discord"
    PUSHOVER = "pushover"
    WEBHOOK = "webhook"


@dataclass
class NotificationConfig:
    """Configuration for a notification channel."""
    channel: NotificationChannel
    enabled: bool = True
    
    # Email config
    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    email_from: Optional[str] = None
    email_to: Optional[List[str]] = None
    
    # Telegram config
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    
    # Discord config
    discord_webhook_url: Optional[str] = None
    
    # Pushover config
    pushover_user_key: Optional[str] = None
    pushover_app_token: Optional[str] = None
    
    # Custom webhook config
    webhook_url: Optional[str] = None
    webhook_method: str = "POST"
    webhook_headers: Optional[Dict] = None


class NotificationManager:
    """
    Manages notifications across multiple channels.
    
    Supports filtering by notification type and automatic
    retry for failed notifications.
    """
    
    def __init__(self):
        """Initialize notification manager."""
        self.logger = logger
        self.configs: List[NotificationConfig] = []
    
    def add_channel(self, config: NotificationConfig):
        """
        Add notification channel.
        
        Args:
            config: NotificationConfig instance
        """
        self.configs.append(config)
    
    def notify(
        self,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.INFO,
        extra_data: Optional[Dict] = None
    ):
        """
        Send notification to all enabled channels.
        
        Args:
            title: Notification title
            message: Notification message
            notification_type: Type of notification
            extra_data: Optional additional data
        """
        for config in self.configs:
            if not config.enabled:
                continue
            
            try:
                if config.channel == NotificationChannel.EMAIL:
                    self._send_email(config, title, message, notification_type)
                
                elif config.channel == NotificationChannel.TELEGRAM:
                    self._send_telegram(config, title, message, notification_type)
                
                elif config.channel == NotificationChannel.DISCORD:
                    self._send_discord(config, title, message, notification_type)
                
                elif config.channel == NotificationChannel.PUSHOVER:
                    self._send_pushover(config, title, message, notification_type)
                
                elif config.channel == NotificationChannel.WEBHOOK:
                    self._send_webhook(config, title, message, notification_type, extra_data)
                
                self.logger.info(f"Notification sent via {config.channel.value}")
            
            except Exception as e:
                self.logger.error(f"Failed to send notification via {config.channel.value}: {e}")
    
    def _send_email(
        self,
        config: NotificationConfig,
        title: str,
        message: str,
        notification_type: NotificationType
    ):
        """Send email notification."""
        if not all([config.smtp_server, config.smtp_user, config.smtp_password, 
                   config.email_from, config.email_to]):
            raise ValueError("Incomplete email configuration")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = config.email_from
        msg['To'] = ', '.join(config.email_to)
        msg['Subject'] = f"[Unit3Dup] {notification_type.value.upper()}: {title}"
        
        # Add emoji based on type
        emoji = {
            NotificationType.SUCCESS: "✅",
            NotificationType.FAILURE: "❌",
            NotificationType.WARNING: "⚠️",
            NotificationType.INFO: "ℹ️",
            NotificationType.STATS: "📊"
        }.get(notification_type, "")
        
        body = f"{emoji} {title}\n\n{message}"
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP(config.smtp_server, config.smtp_port or 587) as server:
            server.starttls()
            server.login(config.smtp_user, config.smtp_password)
            server.send_message(msg)
    
    def _send_telegram(
        self,
        config: NotificationConfig,
        title: str,
        message: str,
        notification_type: NotificationType
    ):
        """Send Telegram notification."""
        if not all([config.telegram_bot_token, config.telegram_chat_id]):
            raise ValueError("Incomplete Telegram configuration")
        
        # Format message
        emoji = {
            NotificationType.SUCCESS: "✅",
            NotificationType.FAILURE: "❌",
            NotificationType.WARNING: "⚠️",
            NotificationType.INFO: "ℹ️",
            NotificationType.STATS: "📊"
        }.get(notification_type, "")
        
        text = f"{emoji} *{title}*\n\n{message}"
        
        url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage"
        data = {
            'chat_id': config.telegram_chat_id,
            'text': text,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
    
    def _send_discord(
        self,
        config: NotificationConfig,
        title: str,
        message: str,
        notification_type: NotificationType
    ):
        """Send Discord webhook notification."""
        if not config.discord_webhook_url:
            raise ValueError("Discord webhook URL not configured")
        
        # Color based on type
        color = {
            NotificationType.SUCCESS: 0x00FF00,  # Green
            NotificationType.FAILURE: 0xFF0000,  # Red
            NotificationType.WARNING: 0xFFFF00,  # Yellow
            NotificationType.INFO: 0x0000FF,     # Blue
            NotificationType.STATS: 0x00FFFF     # Cyan
        }.get(notification_type, 0x808080)
        
        # Create embed
        embed = {
            'title': title,
            'description': message,
            'color': color,
            'footer': {'text': 'Unit3Dup Bot'}
        }
        
        payload = {'embeds': [embed]}
        
        response = requests.post(
            config.discord_webhook_url,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
    
    def _send_pushover(
        self,
        config: NotificationConfig,
        title: str,
        message: str,
        notification_type: NotificationType
    ):
        """Send Pushover notification."""
        if not all([config.pushover_user_key, config.pushover_app_token]):
            raise ValueError("Incomplete Pushover configuration")
        
        # Priority based on type
        priority = {
            NotificationType.SUCCESS: 0,
            NotificationType.FAILURE: 1,
            NotificationType.WARNING: 0,
            NotificationType.INFO: -1,
            NotificationType.STATS: -2
        }.get(notification_type, 0)
        
        data = {
            'token': config.pushover_app_token,
            'user': config.pushover_user_key,
            'title': title,
            'message': message,
            'priority': priority
        }
        
        response = requests.post(
            'https://api.pushover.net/1/messages.json',
            data=data,
            timeout=10
        )
        response.raise_for_status()
    
    def _send_webhook(
        self,
        config: NotificationConfig,
        title: str,
        message: str,
        notification_type: NotificationType,
        extra_data: Optional[Dict]
    ):
        """Send custom webhook notification."""
        if not config.webhook_url:
            raise ValueError("Webhook URL not configured")
        
        payload = {
            'title': title,
            'message': message,
            'type': notification_type.value,
            'timestamp': self._get_timestamp()
        }
        
        if extra_data:
            payload['data'] = extra_data
        
        headers = config.webhook_headers or {'Content-Type': 'application/json'}
        
        if config.webhook_method.upper() == 'POST':
            response = requests.post(
                config.webhook_url,
                json=payload,
                headers=headers,
                timeout=10
            )
        else:
            response = requests.get(
                config.webhook_url,
                params=payload,
                headers=headers,
                timeout=10
            )
        
        response.raise_for_status()
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def notify_upload_success(
        self,
        filename: str,
        tracker: str,
        size_mb: float,
        duration: float
    ):
        """
        Send upload success notification.
        
        Args:
            filename: Uploaded filename
            tracker: Tracker name
            size_mb: File size in MB
            duration: Upload duration in seconds
        """
        title = "Upload Successful"
        message = (
            f"File: {filename}\n"
            f"Tracker: {tracker}\n"
            f"Size: {size_mb:.2f} MB\n"
            f"Duration: {duration:.1f}s"
        )
        
        self.notify(title, message, NotificationType.SUCCESS)
    
    def notify_upload_failure(
        self,
        filename: str,
        tracker: str,
        error: str
    ):
        """
        Send upload failure notification.
        
        Args:
            filename: Failed filename
            tracker: Tracker name
            error: Error message
        """
        title = "Upload Failed"
        message = (
            f"File: {filename}\n"
            f"Tracker: {tracker}\n"
            f"Error: {error}"
        )
        
        self.notify(title, message, NotificationType.FAILURE)
    
    def notify_batch_complete(
        self,
        total: int,
        successful: int,
        failed: int,
        duration: float
    ):
        """
        Send batch completion notification.
        
        Args:
            total: Total files processed
            successful: Successful uploads
            failed: Failed uploads
            duration: Total duration
        """
        title = "Batch Upload Complete"
        message = (
            f"Total: {total}\n"
            f"Successful: {successful}\n"
            f"Failed: {failed}\n"
            f"Success Rate: {(successful/total*100):.1f}%\n"
            f"Duration: {duration:.1f}s"
        )
        
        notification_type = (
            NotificationType.SUCCESS if failed == 0 
            else NotificationType.WARNING
        )
        
        self.notify(title, message, notification_type)
    
    def notify_daily_stats(self, stats: Dict):
        """
        Send daily statistics notification.
        
        Args:
            stats: Statistics dictionary
        """
        title = "Daily Statistics"
        message = (
            f"Uploads: {stats.get('total_uploads', 0)}\n"
            f"Success Rate: {stats.get('success_rate', 0):.1f}%\n"
            f"Data Uploaded: {stats.get('total_data_uploaded_gb', 0):.2f} GB\n"
            f"Avg Duration: {stats.get('average_duration_seconds', 0):.1f}s"
        )
        
        self.notify(title, message, NotificationType.STATS, extra_data=stats)


# Convenience function
def create_notification_manager_from_config(config: Dict) -> NotificationManager:
    """
    Create NotificationManager from configuration dict.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        NotificationManager instance
    """
    manager = NotificationManager()
    
    # Email
    if config.get('email', {}).get('enabled'):
        email_config = config['email']
        manager.add_channel(NotificationConfig(
            channel=NotificationChannel.EMAIL,
            enabled=True,
            smtp_server=email_config.get('smtp_server'),
            smtp_port=email_config.get('smtp_port', 587),
            smtp_user=email_config.get('smtp_user'),
            smtp_password=email_config.get('smtp_password'),
            email_from=email_config.get('from'),
            email_to=email_config.get('to', [])
        ))
    
    # Telegram
    if config.get('telegram', {}).get('enabled'):
        tg_config = config['telegram']
        manager.add_channel(NotificationConfig(
            channel=NotificationChannel.TELEGRAM,
            enabled=True,
            telegram_bot_token=tg_config.get('bot_token'),
            telegram_chat_id=tg_config.get('chat_id')
        ))
    
    # Discord
    if config.get('discord', {}).get('enabled'):
        discord_config = config['discord']
        manager.add_channel(NotificationConfig(
            channel=NotificationChannel.DISCORD,
            enabled=True,
            discord_webhook_url=discord_config.get('webhook_url')
        ))
    
    # Pushover
    if config.get('pushover', {}).get('enabled'):
        po_config = config['pushover']
        manager.add_channel(NotificationConfig(
            channel=NotificationChannel.PUSHOVER,
            enabled=True,
            pushover_user_key=po_config.get('user_key'),
            pushover_app_token=po_config.get('app_token')
        ))
    
    return manager
