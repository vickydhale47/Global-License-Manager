#!/usr/bin/env python3
"""
===============================================================================
Global License Manager - Core License Engine
===============================================================================
Author:         Vicky Dhale
Created:        2024-01-15
Last Modified:  2024-03-20
Version:        1.0.0
Email:          vicky.dhale@outlook.com
GitHub:         @vickydhale

Description:
    Core engine that manages all licensing operations including activation,
    verification, and reporting for Windows and Office products.

Copyright (c) 2024 Vicky Dhale. All rights reserved.
===============================================================================
"""

import os
import sys
import logging
import json
from datetime import datetime
from typing import Dict, Optional, Tuple
from enum import Enum

__author__ = "Vicky Dhale"
__copyright__ = "Copyright 2024, Vicky Dhale"
__credits__ = ["Vicky Dhale"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Vicky Dhale"
__email__ = "vicky.dhale@outlook.com"
__status__ = "Production"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('license_engine.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ActivationType(Enum):
    """Supported activation types"""
    HWID = "HWID"
    KMS38 = "KMS38"
    ONLINE_KMS = "ONLINE_KMS"
    OHOOK = "OHOOK"
    TSFORGE = "TSFORGE"

class LicenseEngine:
    """
    Main license management engine
    Developed by Vicky Dhale
    """
    
    def __init__(self):
        """Initialize the license engine"""
        logger.info("License Engine initialized by Vicky Dhale")
        self.activation_methods = None
        self.system_info = self._get_system_info()
        
    def _get_system_info(self) -> Dict:
        """Get system information"""
        import platform
        import winreg
        
        info = {
            'os': platform.system(),
            'version': platform.version(),
            'build': 0,
            'machine': platform.machine()
        }
        
        # Get Windows build number
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
            )
            info['build'] = int(winreg.QueryValueEx(key, "CurrentBuildNumber")[0])
            winreg.CloseKey(key)
        except:
            pass
            
        return info
    
    def activate(self, activation_type: ActivationType) -> Tuple[bool, str]:
        """
        Activate product using specified method
        
        Args:
            activation_type: Type of activation to perform
            
        Returns:
            Tuple[bool, str]: Success status and message
        """
        logger.info(f"Starting {activation_type.value} activation")
        
        # Import activation methods here to avoid circular imports
        from .activation_methods import ActivationMethods
        self.activation_methods = ActivationMethods()
        
        # Call appropriate method
        if activation_type == ActivationType.HWID:
            return self.activation_methods.hwid_activation()
        elif activation_type == ActivationType.KMS38:
            return self.activation_methods.kms38_activation()
        elif activation_type == ActivationType.ONLINE_KMS:
            return self.activation_methods.online_kms_activation()
        elif activation_type == ActivationType.OHOOK:
            return self.activation_methods.ohook_activation()
        elif activation_type == ActivationType.TSFORGE:
            return self.activation_methods.tsforge_activation()
        else:
            return False, f"Unsupported activation type: {activation_type}"
    
    def get_status(self) -> Dict:
        """Get current license status"""
        logger.info("Getting license status")
        
        status = {
            'product': 'Windows',
            'status': 'Unknown',
            'activation_type': None,
            'remaining_days': 0,
            'last_check': datetime.now().isoformat()
        }
        
        try:
            import subprocess
            result = subprocess.run(
                ['cscript', '//nologo', os.path.expandvars('%SystemRoot%\\System32\\slmgr.vbs'), '/dli'],
                capture_output=True,
                text=True
            )
            
            if 'License Status: Licensed' in result.stdout:
                status['status'] = 'Licensed'
            elif 'License Status: Initial grace period' in result.stdout:
                status['status'] = 'Grace Period'
            else:
                status['status'] = 'Unlicensed'
                
            # Check activation type
            if 'KMS' in result.stdout:
                status['activation_type'] = 'KMS'
            elif 'HWID' in result.stdout:
                status['activation_type'] = 'HWID'
                
        except Exception as e:
            logger.error(f"Failed to get status: {e}")
            
        return status
    
    def generate_report(self) -> str:
        """Generate comprehensive license report"""
        logger.info("Generating license report")
        
        report = f"""
===============================================================================
                GLOBAL LICENSE MANAGER - LICENSE REPORT
===============================================================================
Generated by: Vicky Dhale
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
System: {self.system_info['os']} {self.system_info['build']}

===============================================================================
LICENSE STATUS
===============================================================================
"""
        status = self.get_status()
        report += f"Product: {status['product']}\n"
        report += f"Status: {status['status']}\n"
        report += f"Activation Type: {status['activation_type'] or 'N/A'}\n"
        
        report += """
===============================================================================
END OF REPORT
===============================================================================
Developed by Vicky Dhale - All Rights Reserved
"""
        return report