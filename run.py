#!/usr/bin/env python3
"""
===============================================================================
Global License Manager - Entry Point (EXE Fixed)
===============================================================================
Author:         Vicky Dhale
Version:        1.0.0
===============================================================================
"""

import sys
import os
import traceback
from pathlib import Path

# Fix for PyInstaller
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    print(f"📁 Running from EXE: {BASE_DIR}")
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    print(f"📁 Running from script: {BASE_DIR}")

# Add paths
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

print("🔍 Python path:")
for p in sys.path[:5]:
    print(f"   {p}")

try:
    print("🚀 Importing modules...")
    
    # Import standard libraries first
    print("   - Importing ctypes...")
    import ctypes
    
    print("   - Importing datetime...")
    from datetime import datetime
    
    print("   - Importing PyQt5...")
    from PyQt5.QtWidgets import QApplication
    
    print("   - Importing splash screen...")
    from gui.splash_screen import CyberSplashScreen
    
    print("✅ All imports successful!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    print("\n🔍 Detailed traceback:")
    traceback.print_exc()
    input("\nPress Enter to exit...")
    sys.exit(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Global License Manager")
    app.setApplicationVersion("1.0.0")
    
    splash = CyberSplashScreen()
    splash.show()
    
    sys.exit(app.exec_())