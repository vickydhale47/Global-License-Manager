"""
Utility modules for Global License Manager
Author: Vicky Dhale
"""

from .logger import setup_logger
from .error_handler import ErrorHandler, CriticalError, ConfigurationError, ActivationError

__all__ = ['setup_logger', 'ErrorHandler', 'CriticalError', 'ConfigurationError', 'ActivationError']