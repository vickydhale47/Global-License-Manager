"""
Global License Manager - Logging Utility
Author: Vicky Dhale
"""

import logging
import os
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    """Setup logger with file and console handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Prevent adding duplicate handlers if already configured
    if logger.handlers:
        return logger
        
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # File handler
    log_file = f"logs/{name}_{datetime.now().strftime('%Y%m%d')}.log"
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    fh.setLevel(logging.DEBUG)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    ch.setLevel(logging.INFO)
    
    # Add handlers
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    logger.info(f"Logger initialized for {name} by Vicky Dhale")
    
    return logger