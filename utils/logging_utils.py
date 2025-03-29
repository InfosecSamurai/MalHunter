import logging
import sys
from pathlib import Path

def setup_logging(log_file='malhunter.log'):
    """Configure logging for the application"""
    log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    
    # Create logs directory if it doesn't exist
    log_path = Path(log_file)
    log_path.parent.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Suppress noisy library logs
    logging.getLogger('pefile').setLevel(logging.WARNING)
    logging.getLogger('pyshark').setLevel(logging.WARNING)
