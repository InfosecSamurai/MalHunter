import os
from pathlib import Path

class Settings:
    # Analysis Configuration
    ANALYSIS_TIMEOUT = 60  # seconds
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    
    # Path Configuration
    BASE_DIR = Path(__file__).parent.parent
    YARA_RULES_DIR = BASE_DIR / 'config' / 'yara_rules'
    REPORTS_DIR = BASE_DIR / 'reports'
    
    # Network Configuration
    NETWORK_INTERFACE = 'eth0'
    CAPTURE_TIMEOUT = 30
    
    # External Services
    VT_API_KEY = os.getenv('VT_API_KEY')  # From environment variable
    VT_ENABLED = bool(VT_API_KEY)
    
    @classmethod
    def setup_dirs(cls):
        """Ensure required directories exist"""
        cls.REPORTS_DIR.mkdir(exist_ok=True)
