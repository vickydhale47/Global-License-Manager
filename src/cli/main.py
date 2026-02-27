#!/usr/bin/env python3
"""
===============================================================================
Global License Manager - Command Line Interface
===============================================================================
Author:         Vicky Dhale
Version:        1.0.0
===============================================================================
"""

import os
import sys
import argparse
from pathlib import Path

# Fix Python path - yeh sabse important hai!
current_dir = Path(__file__).parent.absolute()
project_root = current_dir.parent  # src folder
base_dir = project_root.parent      # project root

# Add paths to sys.path
sys.path.insert(0, str(base_dir))
sys.path.insert(0, str(project_root))

print(f"Python Path: {sys.path}")  # Debug - path check karne ke liye

try:
    # Try to import modules
    from src.core.license_engine import LicenseEngine, ActivationType
    from src.utils.logger import setup_logger
    from src.utils.error_handler import ErrorHandler
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check if all __init__.py files exist")
    print("2. Check if files are in correct location")
    print("3. Run: python -c \"import sys; print(sys.path)\"")
    sys.exit(1)

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║             GLOBAL LICENSE MANAGER v1.0.0                ║
    ║                                                           ║
    ║              Developed by: VICKY DHALE                   ║
    ║              Contact: vicky.dhale@outlook.com            ║
    ║              GitHub: @vickydhale                         ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main CLI entry point"""
    print_banner()
    
    # Setup logging
    logger = setup_logger('cli')
    logger.info("Global License Manager CLI started by Vicky Dhale")
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Global License Manager - Developed by Vicky Dhale'
    )
    
    parser.add_argument('--hwid', action='store_true', help='Run HWID activation')
    parser.add_argument('--kms38', action='store_true', help='Run KMS38 activation')
    parser.add_argument('--online-kms', action='store_true', help='Run Online KMS activation')
    parser.add_argument('--ohook', action='store_true', help='Run Ohook activation')
    parser.add_argument('--tsforge', action='store_true', help='Run TSforge activation')
    parser.add_argument('--status', action='store_true', help='Check license status')
    parser.add_argument('--report', action='store_true', help='Generate license report')
    parser.add_argument('--version', action='version', version='Global License Manager 1.0.0')
    
    args = parser.parse_args()
    
    # Initialize engine
    engine = LicenseEngine()
    
    # Handle commands
    if args.hwid:
        print("\n🔑 Running HWID Activation...")
        success, message = engine.activate(ActivationType.HWID)
        print(f"Result: {message}")
    
    elif args.status:
        print("\n📊 License Status")
        status = engine.get_status()
        for key, value in status.items():
            print(f"{key}: {value}")
    
    elif args.report:
        print("\n📄 Generating License Report...")
        report = engine.generate_report()
        print(report)
        
        # Save report
        report_file = "license_report.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"Report saved to: {report_file}")
    
    else:
        parser.print_help()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())