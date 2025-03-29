import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logging(debug=False):
    """Configure application logging"""
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Main logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    # File handler
    log_file = Settings.LOGS_DIR / 'malhunter.log'
    log_file.parent.mkdir(exist_ok=True)
    
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Suppress noisy library logs
    logging.getLogger('pefile').setLevel(logging.WARNING)
    logging.getLogger('pyshark').setLevel(logging.WARNING)
