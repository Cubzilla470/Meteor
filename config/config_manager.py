"""
Configuration management system
"""

import json
import os
from pathlib import Path

class ConfigManager:
    """Manage application configuration"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.meteor_analysis'
        self.config_dir.mkdir(exist_ok=True)
        self.default_config_file = self.config_dir / 'default.json'
        
    def save_config(self, filepath, config_data):
        """Save configuration to file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(config_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False
            
    def load_config(self, filepath):
        """Load configuration from file"""
        try:
            with open(filepath, 'r') as f:
                config_data = json.load(f)
            return config_data
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return None
            
    def load_default_config(self):
        """Load default configuration"""
        if self.default_config_file.exists():
            return self.load_config(str(self.default_config_file))
        else:
            return self.get_default_config()
            
    def get_default_config(self):
        """Get default configuration dictionary"""
        return {
            'sensitivity': 1.0,
            'threshold': 50,
            'min_duration': 0.1,
            'classification_filter': 'All Types',
            'show_confidence': True,
            'resizable_windows': True,
            'dark_mode': True,
            'video_path': '',
            'zoom_level': 1.0,
            'show_light_curve': True,
            'show_motion': True,
            'show_confidence_band': True,
        }
