# -*- coding: utf-8 -*-
"""
Web Dashboard for Unit3Dup

Simple Flask-based web interface for:
- Viewing upload statistics
- Monitoring batch progress
- Managing configuration
- Viewing logs
- Manual uploads

Requirements:
pip install flask flask-cors
"""

try:
    from flask import Flask, render_template, jsonify, request, send_file
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    Flask = None

import json
from pathlib import Path
from typing import Optional
import threading

from common.upload_stats import get_stats_manager
from common.logger import get_logger
from common.config_manager import get_config


logger = get_logger(__name__)


class WebDashboard:
    """
    Web dashboard for Unit3Dup.
    
    Provides a simple web interface for monitoring and management.
    """
    
    def __init__(self, host: str = '127.0.0.1', port: int = 5000):
        """
        Initialize web dashboard.
        
        Args:
            host: Host to bind to
            port: Port to bind to
        """
        if not FLASK_AVAILABLE:
            raise ImportError(
                "Flask is required for web interface. "
                "Install with: pip install flask flask-cors"
            )
        
        self.host = host
        self.port = port
        self.app = Flask(__name__, 
                        template_folder=str(Path(__file__).parent / 'templates'),
                        static_folder=str(Path(__file__).parent / 'static'))
        
        CORS(self.app)  # Enable CORS
        
        self.stats_manager = get_stats_manager()
        self.logger = logger
        
        # Setup routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/')
        def index():
            """Dashboard home page."""
            return render_template('dashboard.html')
        
        @self.app.route('/api/stats')
        def get_stats():
            """Get upload statistics."""
            days = request.args.get('days', default=7, type=int)
            stats = self.stats_manager.get_stats(days=days)
            return jsonify(stats)
        
        @self.app.route('/api/stats/history')
        def get_history():
            """Get upload history."""
            limit = request.args.get('limit', default=50, type=int)
            history = self.stats_manager.get_upload_history(limit=limit)
            return jsonify(history)
        
        @self.app.route('/api/config')
        def get_config_api():
            """Get configuration (sanitized)."""
            try:
                config = get_config()
                
                # Sanitize sensitive data
                config_dict = {
                    'trackers': list(config.tracker_config.MULTI_TRACKER),
                    'torrent_client': config.torrent_client_config.TORRENT_CLIENT,
                    'user_preferences': {
                        'number_of_screenshots': config.user_preferences.NUMBER_OF_SCREENSHOTS,
                        'duplicate_on': config.user_preferences.DUPLICATE_ON,
                        'skip_duplicate': config.user_preferences.SKIP_DUPLICATE,
                        'watcher_interval': config.user_preferences.WATCHER_INTERVAL,
                        'anon': config.user_preferences.ANON
                    }
                }
                
                return jsonify(config_dict)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/logs')
        def get_logs():
            """Get recent logs."""
            try:
                # Read last 100 lines of log file
                log_file = Path.home() / ".unit3dup" / "unit3dup.log"
                
                if not log_file.exists():
                    return jsonify({'logs': []})
                
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    recent_logs = lines[-100:]
                
                return jsonify({'logs': recent_logs})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/health')
        def health_check():
            """Health check endpoint."""
            return jsonify({
                'status': 'ok',
                'version': '0.8.23',
                'uptime': 'N/A'
            })
    
    def run(self, debug: bool = False, threaded: bool = True):
        """
        Run web server.
        
        Args:
            debug: Enable debug mode
            threaded: Enable threading
        """
        self.logger.info(f"Starting web dashboard on http://{self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=debug, threaded=threaded)
    
    def run_in_background(self):
        """Run web server in background thread."""
        thread = threading.Thread(target=self.run, kwargs={'debug': False})
        thread.daemon = True
        thread.start()
        self.logger.info(f"Web dashboard running in background on http://{self.host}:{self.port}")


# Convenience function
def start_web_dashboard(host: str = '127.0.0.1', port: int = 5000, background: bool = False):
    """
    Start web dashboard.
    
    Args:
        host: Host to bind to
        port: Port to bind to
        background: Run in background thread
    """
    dashboard = WebDashboard(host, port)
    
    if background:
        dashboard.run_in_background()
    else:
        dashboard.run()


if __name__ == '__main__':
    start_web_dashboard()
