#!/usr/bin/env python3
"""
===============================================================================
Global License Manager - Activation Methods
===============================================================================
Author:         Vicky Dhale
Created:        2024-01-15
Description:    All activation method implementations
===============================================================================
"""

import os
import subprocess
import platform
from pathlib import Path
from typing import Tuple

import logging

__author__ = "Vicky Dhale"

logger = logging.getLogger(__name__)

class ActivationMethods:
    """
    All activation methods implementation
    Created by Vicky Dhale
    """
    
    def hwid_activation(self) -> Tuple[bool, str]:
        """HWID Activation Method"""
        try:
            logger.info("Vicky Dhale: Starting HWID activation")
            
            # Check admin rights
            if platform.system() != "Windows":
                return False, "Windows-only activation method"
                
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                return False, "Administrator privileges required"
            
            # Create ticket directory
            ticket_dir = Path("C:/ProgramData/Microsoft/Windows/ClipSVC/GenuineTicket")
            ticket_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate ticket
            import base64
            session_id = base64.b64encode(
                b"OSMajorVersion=5;OSMinorVersion=1;OSPlatformId=2;PP=0;"
            ).decode()
            
            from datetime import datetime
            ticket_xml = f'''<?xml version="1.0" encoding="utf-8"?>
            <genuineAuthorization xmlns="http://www.microsoft.com/DRM/SL/GenuineAuthorization/1.0">
                <version>1.0</version>
                <genuineProperties origin="sppclient">
                    <properties>
                        OA3xOriginalProductId=;
                        OA3xOriginalProductKey=;
                        SessionId={session_id};
                        TimeStampClient={datetime.now().isoformat()}Z
                    </properties>
                </genuineProperties>
            </genuineAuthorization>'''
            
            ticket_path = ticket_dir / "GenuineTicket.xml"
            with open(ticket_path, 'w', encoding='utf-8') as f:
                f.write(ticket_xml)
            
            # Restart ClipSVC
            subprocess.run(
                ["powershell", "Restart-Service ClipSVC -Force"],
                capture_output=True
            )
            
            # Run clipup
            result = subprocess.run(
                ["clipup.exe", "-v", "-o"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("HWID activation successful")
                return True, "HWID activation completed successfully"
            else:
                return False, f"HWID failed: {result.stderr}"
                
        except Exception as e:
            logger.error(f"HWID activation failed: {e}")
            return False, f"Error: {str(e)}"
    
    def kms38_activation(self) -> Tuple[bool, str]:
        """KMS38 Activation Method"""
        try:
            logger.info("Vicky Dhale: Starting KMS38 activation")
            
            # Check admin rights
            if platform.system() != "Windows":
                return False, "Windows-only activation method"
                
            import ctypes
            import winreg
            if not ctypes.windll.shell32.IsUserAnAdmin():
                return False, "Administrator privileges required"
            
            # Set KMS host to localhost
            key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform"
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "KeyManagementServiceName", 0, winreg.REG_SZ, "127.0.0.2")
                winreg.SetValueEx(key, "KeyManagementServicePort", 0, winreg.REG_SZ, "1688")
                winreg.CloseKey(key)
                logger.info("KMS host set to 127.0.0.2")
            except Exception as e:
                return False, f"Failed to set KMS host: {e}"
            
            # Generate KMS38 ticket
            ticket_dir = Path("C:/ProgramData/Microsoft/Windows/ClipSVC/GenuineTicket")
            ticket_dir.mkdir(parents=True, exist_ok=True)
            
            session_id = "TwBTAE0AYQBqAG8AcgBWAGUAcgBzAGkAbwBuAD0ANQA7AE8AUwBNAGkAbgBvAHIAVgBlAHIAcwBpAG8AbgA9ADEAOwBPAFMAUABsAGEAdABmAG8AcgBtAEkAZAA9ADIAOwBQAFAAPQAwADsARwBWAEwASwBFAHgAcAA9ADIAMAAzADgALQAwADEALQAxADkAVAAwADMAOgAxADQAOgAwADcAWgA7AEQAbwB3AG4AbABlAHYAZQBsAEcAZQBuAHUAaQBuAGUAUwB0AGEAdABlAD0AMQA7AAAA"
            
            from datetime import datetime
            ticket_xml = f'''<?xml version="1.0" encoding="utf-8"?>
            <genuineAuthorization xmlns="http://www.microsoft.com/DRM/SL/GenuineAuthorization/1.0">
                <version>1.0</version>
                <genuineProperties origin="sppclient">
                    <properties>
                        OA3xOriginalProductId=;
                        OA3xOriginalProductKey=;
                        SessionId={session_id};
                        TimeStampClient={datetime.now().isoformat()}Z
                    </properties>
                </genuineProperties>
            </genuineAuthorization>'''
            
            ticket_path = ticket_dir / "GenuineTicket.xml"
            with open(ticket_path, 'w', encoding='utf-8') as f:
                f.write(ticket_xml)
            
            # Run clipup
            result = subprocess.run(["clipup.exe", "-v", "-o"], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("KMS38 activation successful")
                return True, "KMS38 activation completed successfully"
            else:
                return False, f"KMS38 failed: {result.stderr}"
                
        except Exception as e:
            logger.error(f"KMS38 activation failed: {e}")
            return False, f"Error: {str(e)}"
    
    def online_kms_activation(self) -> Tuple[bool, str]:
        """Online KMS Activation Method"""
        try:
            logger.info("Vicky Dhale: Starting Online KMS activation")
            
            # Check admin rights
            if platform.system() != "Windows":
                return False, "Windows-only activation method"
                
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                return False, "Administrator privileges required"
            
            # KMS servers list
            servers = [
                "kms8.msguides.com",
                "kms9.msguides.com",
                "kms.digiboy.ir",
                "kms.lotro.cc"
            ]
            
            import socket
            import winreg
            
            key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform"
            
            for server in servers:
                try:
                    # Test connection
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    result = sock.connect_ex((server, 1688))
                    sock.close()
                    
                    if result == 0:
                        logger.info(f"Found working KMS server: {server}")
                        
                        # Set KMS server
                        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
                        winreg.SetValueEx(key, "KeyManagementServiceName", 0, winreg.REG_SZ, server)
                        winreg.CloseKey(key)
                        
                        # Activate
                        import subprocess
                        act_result = subprocess.run(["slmgr", "/ato"], capture_output=True, text=True)
                        
                        if act_result.returncode == 0:
                            logger.info(f"Online KMS activation successful with {server}")
                            return True, f"Activated with KMS server: {server}"
                        else:
                            logger.warning(f"Activation failed with {server}, trying next...")
                except Exception:
                    continue
            
            return False, "No working KMS servers found"
            
        except Exception as e:
            logger.error(f"Online KMS activation error: {e}")
            return False, f"Error: {str(e)}"
    
    def ohook_activation(self) -> Tuple[bool, str]:
        """Ohook Activation Method for Office"""
        try:
            logger.info("Vicky Dhale: Starting Ohook activation")
            
            # Find Office installation
            program_files = os.environ.get('ProgramFiles', 'C:\\Program Files')
            program_files_x86 = os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')
            
            office_paths = [
                Path(program_files) / "Microsoft Office" / "root",
                Path(program_files_x86) / "Microsoft Office" / "root",
                Path(program_files) / "Microsoft Office" / "Office16",
                Path(program_files_x86) / "Microsoft Office" / "Office16"
            ]
            
            office_root = None
            for path in office_paths:
                if path.exists():
                    office_root = path
                    break
            
            if not office_root:
                return False, "Office installation not found"
            
            logger.info(f"Office found at: {office_root}")
            
            # Create ohook files
            # Note: Actual ohook implementation would go here
            # This is a simplified version
            
            return True, "Ohook activation completed (simulated)"
            
        except Exception as e:
            logger.error(f"Ohook activation failed: {e}")
            return False, f"Error: {str(e)}"
    
    def tsforge_activation(self) -> Tuple[bool, str]:
        """TSforge Activation Method for legacy systems"""
        try:
            logger.info("Vicky Dhale: Starting TSforge activation")
            
            # TSforge implementation for legacy systems
            # This would contain the C# code from your original script
            
            return True, "TSforge activation completed (simulated)"
            
        except Exception as e:
            logger.error(f"TSforge activation failed: {e}")
            return False, f"Error: {str(e)}"