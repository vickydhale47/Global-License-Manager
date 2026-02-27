#!/usr/bin/env python3
"""
===============================================================================
Global License Manager - About Dialog
===============================================================================
Author:         Vicky Dhale
Created:        2024-01-15
Description:    About dialog showing developer information
===============================================================================
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QIcon

__author__ = "Vicky Dhale"

class AboutDialog(QDialog):
    """About dialog showing Vicky Dhale as developer"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Global License Manager")
        self.setFixedSize(500, 400)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Global License Manager")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Developer info
        dev_label = QLabel("Developed by")
        dev_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(dev_label)
        
        # Vicky Dhale name
        name_label = QLabel("VICKY DHALE")
        name_font = QFont()
        name_font.setPointSize(14)
        name_font.setBold(True)
        name_label.setFont(name_font)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(name_label)
        
        # Version
        version = QLabel("Version 1.0.0")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)
        
        # Separator
        line = QLabel("─" * 50)
        line.setAlignment(Qt.AlignCenter)
        layout.addWidget(line)
        
        # Contact info
        contact_title = QLabel("Contact Information:")
        contact_title.setStyleSheet("font-weight: bold;")
        layout.addWidget(contact_title)
        
        email = QLabel("📧 Email: vicky.dhale@outlook.com")
        layout.addWidget(email)
        
        github = QLabel("🐙 GitHub: @vickydhale")
        layout.addWidget(github)
        
        linkedin = QLabel("💼 LinkedIn: Vicky Dhale")
        layout.addWidget(linkedin)
        
        # Separator
        line2 = QLabel("─" * 50)
        line2.setAlignment(Qt.AlignCenter)
        layout.addWidget(line2)
        
        # Copyright
        copyright = QLabel("© 2024 Vicky Dhale. All Rights Reserved.")
        copyright.setAlignment(Qt.AlignCenter)
        layout.addWidget(copyright)
        
        # OK button
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.setFixedWidth(100)
        ok_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)