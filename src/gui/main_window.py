#!/usr/bin/env python3
"""
===============================================================================
Global License Manager - Professional UI (FINAL)
===============================================================================
Author:         Vicky Dhale
Version:        1.0.0
Description:    Professional dark interface with perfect styling
===============================================================================
"""

import sys
import os
import ctypes
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QTextEdit, QMessageBox, QTabWidget,
    QGroupBox, QGridLayout, QProgressBar, QStatusBar, QSplitter,
    QListWidget, QListWidgetItem, QComboBox, QLineEdit, QCheckBox,
    QSpinBox, QMenuBar, QMenu, QAction, QToolBar, QToolButton,
    QScrollArea, QSizePolicy, QFormLayout, QFileDialog, QDialog,
    QDialogButtonBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QColor

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.license_engine import LicenseEngine, ActivationType

# ==================== DARK MESSAGE BOX ====================
class DarkMessageBox(QMessageBox):
    """Custom dark message box for consistent theming"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QMessageBox {
                background-color: #1a1a1a;
            }
            QMessageBox QLabel {
                color: #e0e0e0;
                font-size: 10pt;
                min-width: 300px;
            }
            QMessageBox QPushButton {
                background-color: #00a8e8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 10pt;
                font-weight: 500;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #0090c0;
            }
            QMessageBox QPushButton[text="Cancel"] {
                background-color: #2a2a2a;
                border: 1px solid #444444;
            }
            QMessageBox QPushButton[text="Cancel"]:hover {
                background-color: #3a3a3a;
            }
        """)

class ActivationThread(QThread):
    finished = pyqtSignal(bool, str)
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    
    def __init__(self, engine, method):
        super().__init__()
        self.engine = engine
        self.method = method
        
    def run(self):
        try:
            self.log.emit(f"▶ Starting {self.method.value}...")
            self.progress.emit(20)
            
            if not ctypes.windll.shell32.IsUserAnAdmin():
                self.log.emit("⛔ Admin required!")
                self.finished.emit(False, "Admin required")
                return
            
            self.progress.emit(40)
            success, message = self.engine.activate(self.method)
            self.progress.emit(80)
            
            if success:
                self.log.emit(f"✓ {message}")
            else:
                self.log.emit(f"✗ {message}")
            
            self.progress.emit(100)
            self.finished.emit(success, message)
            
        except Exception as e:
            self.log.emit(f"✗ Error: {str(e)}")
            self.finished.emit(False, str(e))

class ModernButton(QPushButton):
    """Custom modern button with hover effects"""
    def __init__(self, text, parent=None, primary=False, compact=False, clicked=None):
        super().__init__(text, parent)
        self.primary = primary
        self.compact = compact
        self.setCursor(Qt.PointingHandCursor)
        
        if clicked:
            self.clicked.connect(clicked)
        
        if compact:
            self.setMinimumHeight(28)
            self.setStyleSheet("""
                QPushButton {
                    background-color: #1e1e1e;
                    border: 1px solid #333333;
                    color: #e0e0e0;
                    border-radius: 4px;
                    font-weight: 500;
                    font-size: 9pt;
                    padding: 4px 8px;
                    text-align: left;
                }
                QPushButton:hover {
                    border-color: #00a8e8;
                    color: #00a8e8;
                    background-color: #2a2a2a;
                }
            """)
        elif primary:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #00a8e8;
                    border: none;
                    color: white;
                    border-radius: 4px;
                    font-weight: 600;
                    font-size: 10pt;
                    padding: 8px 15px;
                }
                QPushButton:hover {
                    background-color: #0090c0;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #1e1e1e;
                    border: 1px solid #333333;
                    color: #e0e0e0;
                    border-radius: 4px;
                    font-weight: 500;
                    font-size: 10pt;
                    padding: 8px 15px;
                }
                QPushButton:hover {
                    border-color: #00a8e8;
                    color: #00a8e8;
                }
            """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = LicenseEngine()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Global License Manager - Professional Edition")
        self.setMinimumSize(1200, 700)
        self.showMaximized()
        
        # Set window icon
        icon_path = Path(__file__).parent.parent.parent / "icon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # 🎯 PROFESSIONAL DARK THEME
        self.setStyleSheet("""
            /* Main Window */
            QMainWindow {
                background-color: #0a0a0a;
            }
            
            /* Menu Bar */
            QMenuBar {
                background-color: #1a1a1a;
                color: #e0e0e0;
                border-bottom: 1px solid #333333;
                min-height: 28px;
                font-size: 10pt;
            }
            QMenuBar::item {
                padding: 5px 15px;
                border-radius: 3px;
            }
            QMenuBar::item:selected {
                background-color: #00a8e8;
                color: white;
            }
            QMenu {
                background-color: #1a1a1a;
                color: #e0e0e0;
                border: 1px solid #333333;
                font-size: 10pt;
            }
            QMenu::item {
                padding: 5px 25px;
            }
            QMenu::item:selected {
                background-color: #00a8e8;
            }
            
            /* Toolbar */
            QToolBar {
                background-color: #1a1a1a;
                border: none;
                min-height: 36px;
                spacing: 2px;
                padding: 2px;
            }
            QToolButton {
                color: #e0e0e0;
                padding: 5px 12px;
                border-radius: 3px;
                font-size: 10pt;
            }
            QToolButton:hover {
                background-color: #00a8e8;
                color: white;
            }
            
            /* Tabs */
            QTabWidget::pane {
                background-color: #1a1a1a;
                border: 1px solid #333333;
                border-radius: 4px;
                margin-top: -1px;
            }
            QTabBar::tab {
                background-color: transparent;
                color: #888888;
                padding: 8px 22px;
                font-size: 10pt;
                min-width: 120px;
                min-height: 32px;
            }
            QTabBar::tab:selected {
                color: #00a8e8;
                border-bottom: 3px solid #00a8e8;
                background-color: #111111;
            }
            QTabBar::tab:hover {
                color: white;
            }
            
            /* Labels */
            QLabel {
                color: #e0e0e0;
                font-size: 10pt;
            }
            QLabel#header {
                color: white;
                font-size: 22px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
            QLabel#author {
                color: white;
                font-size: 12px;
                font-weight: 700;
                background-color: #2a2a2a;
                padding: 5px 18px;
                border-radius: 20px;
                border: 1px solid #444444;
            }
            QLabel#section-title {
                color: #888888;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 0.5px;
                padding: 2px 0;
            }
            QLabel#status-text {
                color: #4caf50;
                font-size: 10pt;
                padding: 2px;
            }
            
            /* List Widget */
            QListWidget {
                background-color: #1a1a1a;
                color: #e0e0e0;
                border: 1px solid #333333;
                border-radius: 3px;
                font-size: 9pt;
                padding: 3px;
            }
            QListWidget::item {
                padding: 3px;
                border-radius: 2px;
            }
            QListWidget::item:selected {
                background-color: #00a8e8;
            }
            
            /* Text Edit */
            QTextEdit {
                background-color: #0a0a0a;
                color: #4caf50;
                border: 1px solid #333333;
                border-radius: 3px;
                font-family: 'Consolas', monospace;
                font-size: 9pt;
                padding: 5px;
            }
            
            /* Input Fields */
            QLineEdit, QComboBox, QSpinBox {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #333333;
                border-radius: 3px;
                padding: 4px;
                font-size: 9pt;
                min-height: 22px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: #00a8e8;
            }
            
            /* Checkbox */
            QCheckBox {
                color: #e0e0e0;
                font-size: 9pt;
                spacing: 4px;
            }
            QCheckBox::indicator {
                width: 14px;
                height: 14px;
                border: 2px solid #333333;
                border-radius: 3px;
                background-color: #1e1e1e;
            }
            QCheckBox::indicator:checked {
                background-color: #00a8e8;
            }
            
            /* Group Box */
            QGroupBox {
                color: #00a8e8;
                border: 1px solid #333333;
                border-radius: 4px;
                margin-top: 6px;
                font-weight: 600;
                font-size: 10pt;
                padding-top: 6px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 6px;
                padding: 0 4px 0 4px;
                color: #00a8e8;
            }
            
            /* Progress Bar */
            QProgressBar {
                border: none;
                border-radius: 2px;
                background-color: #2a2a2a;
                height: 3px;
            }
            QProgressBar::chunk {
                background-color: #00a8e8;
                border-radius: 2px;
            }
            
            /* Status Bar */
            QStatusBar {
                background-color: #1a1a1a;
                color: #888888;
                border-top: 1px solid #333333;
                min-height: 22px;
                font-size: 9pt;
            }
            
            /* Splitter */
            QSplitter::handle {
                background-color: #333333;
                width: 1px;
            }
            
            /* Frames */
            QFrame#card {
                background-color: #1a1a1a;
                border-radius: 5px;
            }
            QFrame#info-card {
                background-color: #1e1e1e;
                border-radius: 4px;
                padding: 6px;
            }
        """)
        
        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        file_menu.addAction('Save Report', self.save_report)
        file_menu.addAction('Export Logs', self.export_logs)
        file_menu.addSeparator()
        file_menu.addAction('Exit', self.close)
        
        act_menu = menubar.addMenu('Activation')
        act_menu.addAction('HWID', lambda: self.start_activation(ActivationType.HWID))
        act_menu.addAction('KMS38', lambda: self.start_activation(ActivationType.KMS38))
        act_menu.addAction('Online KMS', lambda: self.start_activation(ActivationType.ONLINE_KMS))
        act_menu.addSeparator()
        act_menu.addAction('Ohook', lambda: self.start_activation(ActivationType.OHOOK))
        act_menu.addAction('TSforge', lambda: self.start_activation(ActivationType.TSFORGE))
        
        tools_menu = menubar.addMenu('Tools')
        tools_menu.addAction('Refresh Status', self.refresh_status)
        tools_menu.addAction('Check System', self.check_system)
        
        help_menu = menubar.addMenu('Help')
        help_menu.addAction('Documentation', self.show_docs)
        help_menu.addSeparator()
        help_menu.addAction('About', self.show_about)
        
        # Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(False)
        for text, callback in [
            ("🔑 HWID", lambda: self.start_activation(ActivationType.HWID)),
            ("🔒 KMS38", lambda: self.start_activation(ActivationType.KMS38)),
            ("🌐 Online", lambda: self.start_activation(ActivationType.ONLINE_KMS)),
            ("📝 Ohook", lambda: self.start_activation(ActivationType.OHOOK)),
            ("🔄 Refresh", self.refresh_status),
            ("📊 Report", self.generate_report)
        ]:
            toolbar.addAction(text, callback)
        self.addToolBar(toolbar)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(10, 5, 10, 5)
        
        # HEADER
        header = QWidget()
        header.setFixedHeight(55)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Logo
        logo_path = Path(__file__).parent.parent.parent / "logo.png"
        if logo_path.exists():
            logo = QLabel()
            pixmap = QPixmap(str(logo_path)).scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
            header_layout.addWidget(logo)
        
        # Title
        title = QLabel("GLOBAL LICENSE MANAGER")
        title.setObjectName("header")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Author
        author = QLabel("Author : Vicky Dhale")
        author.setObjectName("author")
        header_layout.addWidget(author)
        
        main_layout.addWidget(header)
        
        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(1)
        splitter.setChildrenCollapsible(False)
        
        # LEFT PANEL
        left_panel = QFrame()
        left_panel.setObjectName("card")
        left_panel.setFixedWidth(240)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(6)
        left_layout.setContentsMargins(8, 8, 8, 8)
        
        # Quick Actions
        left_layout.addWidget(QLabel("QUICK ACTIONS", objectName="section-title"))
        left_layout.addWidget(ModernButton("📊 Check Status", compact=True, 
                                          clicked=lambda: self.tabs.setCurrentIndex(1)))
        left_layout.addWidget(ModernButton("📄 Generate Report", compact=True, 
                                          clicked=lambda: self.tabs.setCurrentIndex(2)))
        
        left_layout.addSpacing(4)
        
        # Recent Activities
        left_layout.addWidget(QLabel("RECENT ACTIVITIES", objectName="section-title"))
        self.recent_list = QListWidget()
        self.recent_list.setMaximumHeight(65)
        self.recent_list.addItem("▶ Program started")
        left_layout.addWidget(self.recent_list)
        
        left_layout.addSpacing(4)
        
        # System Information
        left_layout.addWidget(QLabel("SYSTEM INFORMATION", objectName="section-title"))
        sys_frame = QFrame()
        sys_frame.setObjectName("info-card")
        sys_layout = QVBoxLayout(sys_frame)
        sys_layout.setSpacing(2)
        sys_layout.setContentsMargins(6, 6, 6, 6)
        
        self.sys_info = QLabel()
        self.sys_info.setObjectName("status-text")
        self.sys_info.setWordWrap(True)
        sys_layout.addWidget(self.sys_info)
        left_layout.addWidget(sys_frame)
        
        left_layout.addSpacing(4)
        
        # Navigation
        left_layout.addWidget(QLabel("NAVIGATION", objectName="section-title"))
        nav_items = [
            ("⚡ Activation", 0),
            ("📊 Status", 1),
            ("📄 Reports", 2),
            ("⚙️ Settings", 3),
            ("ℹ️ About", 4)
        ]
        for text, idx in nav_items:
            btn = ModernButton(text, compact=True, clicked=lambda i=idx: self.tabs.setCurrentIndex(i))
            left_layout.addWidget(btn)
        
        left_layout.addStretch()
        
        # RIGHT PANEL
        right_panel = QFrame()
        right_panel.setObjectName("card")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(6, 6, 6, 6)
        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        
        # TAB 1: Activation
        act_tab = QWidget()
        act_layout = QVBoxLayout(act_tab)
        act_layout.setSpacing(5)
        act_layout.setContentsMargins(6, 6, 6, 6)
        
        # Windows Activation
        win_group = QGroupBox("WINDOWS ACTIVATION")
        win_grid = QGridLayout(win_group)
        win_grid.setSpacing(5)
        win_grid.setContentsMargins(6, 6, 6, 6)
        
        # 2x2 Grid
        methods = [
            ("🔑 HWID", "Windows 10/11 · Permanent", ActivationType.HWID),
            ("🔒 KMS38", "Valid until 2038 · Offline", ActivationType.KMS38),
            ("🌐 Online KMS", "180 days · Auto-renewal", ActivationType.ONLINE_KMS),
            ("⚙️ TSforge", "Windows 7/8/8.1 · Legacy", ActivationType.TSFORGE)
        ]
        
        for i, (title, desc, method) in enumerate(methods):
            row, col = i // 2, i % 2
            method_widget = self.create_method_widget(title, desc, method)
            win_grid.addWidget(method_widget, row, col)
        
        act_layout.addWidget(win_group)
        
        # Office Activation
        office_group = QGroupBox("OFFICE ACTIVATION")
        office_layout = QHBoxLayout(office_group)
        office_layout.setContentsMargins(6, 6, 6, 6)
        
        ohook_widget = self.create_method_widget(
            "📝 OHOOK",
            "Office 2016-2024 · Permanent · All editions",
            ActivationType.OHOOK,
            primary=True
        )
        office_layout.addWidget(ohook_widget)
        
        act_layout.addWidget(office_group)
        
        # Advanced Options
        adv_group = QGroupBox("ADVANCED OPTIONS")
        adv_layout = QGridLayout(adv_group)
        adv_layout.setSpacing(4)
        adv_layout.setContentsMargins(6, 6, 6, 6)
        
        adv_layout.addWidget(QLabel("KMS Server:"), 0, 0)
        self.kms_server = QLineEdit()
        self.kms_server.setPlaceholderText("kms.example.com")
        adv_layout.addWidget(self.kms_server, 0, 1)
        
        adv_layout.addWidget(QLabel("KMS Port:"), 1, 0)
        self.kms_port = QSpinBox()
        self.kms_port.setRange(1, 65535)
        self.kms_port.setValue(1688)
        adv_layout.addWidget(self.kms_port, 1, 1)
        
        self.auto_renew = QCheckBox("Enable auto-renewal task")
        adv_layout.addWidget(self.auto_renew, 2, 0, 1, 2)
        
        act_layout.addWidget(adv_group)
        act_layout.addStretch()
        
        self.tabs.addTab(act_tab, "⚡ Activation")
        
        # TAB 2: Status
        status_tab = QWidget()
        status_layout = QVBoxLayout(status_tab)
        status_layout.setContentsMargins(6, 6, 6, 6)
        
        refresh_btn = ModernButton("🔄 Refresh Status", compact=True, clicked=self.refresh_status)
        refresh_btn.setMaximumWidth(100)
        status_layout.addWidget(refresh_btn, alignment=Qt.AlignRight)
        
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        status_layout.addWidget(self.status_display)
        
        self.tabs.addTab(status_tab, "📊 Status")
        
        # TAB 3: Reports
        report_tab = QWidget()
        report_layout = QVBoxLayout(report_tab)
        report_layout.setContentsMargins(6, 6, 6, 6)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(ModernButton("📊 Generate Report", compact=True, clicked=self.generate_report))
        btn_layout.addWidget(ModernButton("💾 Save Report", compact=True, clicked=self.save_report))
        btn_layout.addStretch()
        report_layout.addLayout(btn_layout)
        
        self.report_display = QTextEdit()
        self.report_display.setReadOnly(True)
        report_layout.addWidget(self.report_display)
        
        self.tabs.addTab(report_tab, "📄 Reports")
        
        # TAB 4: Settings
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        settings_layout.setSpacing(5)
        settings_layout.setContentsMargins(6, 6, 6, 6)
        
        # General Settings
        general_group = QGroupBox("GENERAL SETTINGS")
        general_form = QFormLayout(general_group)
        general_form.setSpacing(4)
        general_form.setContentsMargins(6, 6, 6, 6)
        
        self.auto_refresh = QCheckBox("Enable auto-refresh")
        self.auto_refresh.setChecked(True)
        general_form.addRow("Auto Refresh:", self.auto_refresh)
        
        self.refresh_int = QSpinBox()
        self.refresh_int.setRange(10, 300)
        self.refresh_int.setValue(30)
        self.refresh_int.setSuffix("s")
        general_form.addRow("Interval:", self.refresh_int)
        
        self.save_logs = QCheckBox("Save logs to file")
        self.save_logs.setChecked(True)
        general_form.addRow("Save Logs:", self.save_logs)
        
        settings_layout.addWidget(general_group)
        
        # KMS Settings
        kms_group = QGroupBox("KMS SETTINGS")
        kms_form = QFormLayout(kms_group)
        kms_form.setSpacing(4)
        kms_form.setContentsMargins(6, 6, 6, 6)
        
        self.default_kms = QLineEdit()
        self.default_kms.setPlaceholderText("kms8.msguides.com")
        kms_form.addRow("Server:", self.default_kms)
        
        self.default_port = QSpinBox()
        self.default_port.setRange(1, 65535)
        self.default_port.setValue(1688)
        kms_form.addRow("Port:", self.default_port)
        
        self.auto_kms = QCheckBox("Auto-discover servers")
        self.auto_kms.setChecked(True)
        kms_form.addRow("Discovery:", self.auto_kms)
        
        settings_layout.addWidget(kms_group)
        
        settings_layout.addWidget(ModernButton("💾 Save Settings", primary=True, 
                                              clicked=self.save_settings))
        settings_layout.addStretch()
        
        self.tabs.addTab(settings_tab, "⚙️ Settings")
        
        # TAB 5: About (WITH LOGO)
        about_tab = QWidget()
        about_layout = QVBoxLayout(about_tab)
        about_layout.setSpacing(8)
        about_layout.setContentsMargins(15, 15, 15, 15)
        
        about_layout.addStretch()
        
        # ===== LOGO =====
        logo_path = Path(__file__).parent.parent.parent / "logo.png"
        if logo_path.exists():
            logo_label = QLabel()
            pixmap = QPixmap(str(logo_path))
            # Resize logo to reasonable size (120x120)
            scaled_pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            about_layout.addWidget(logo_label)
            about_layout.addSpacing(10)
        
        # Title
        title = QLabel("GLOBAL LICENSE MANAGER")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #00a8e8;")
        title.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(title)
        
        # Version
        version = QLabel("Professional Edition v1.0.0")
        version.setStyleSheet("font-size: 12px; color: #888888;")
        version.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(version)
        
        about_layout.addSpacing(20)
        
        # Developer Card
        dev_card = QFrame()
        dev_card.setObjectName("info-card")
        dev_card.setStyleSheet("""
            QFrame#info-card {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 15px;
                border: 1px solid #333333;
            }
        """)
        dev_layout = QVBoxLayout(dev_card)
        dev_layout.setSpacing(8)
        
        # Developer icon
        dev_icon = QLabel("👨‍💻")
        dev_icon.setStyleSheet("font-size: 32px;")
        dev_icon.setAlignment(Qt.AlignCenter)
        dev_layout.addWidget(dev_icon)
        
        dev_layout.addWidget(QLabel("DEVELOPER"), alignment=Qt.AlignCenter)
        
        name_label = QLabel("Vicky Dhale")
        name_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #00a8e8;")
        name_label.setAlignment(Qt.AlignCenter)
        dev_layout.addWidget(name_label)
        
        dev_layout.addSpacing(5)
        
        email_label = QLabel("📧 vicky.dhale@outlook.com")
        email_label.setStyleSheet("color: #888888;")
        email_label.setAlignment(Qt.AlignCenter)
        dev_layout.addWidget(email_label)
        
        github_label = QLabel("🐙 @vickydhale")
        github_label.setStyleSheet("color: #888888;")
        github_label.setAlignment(Qt.AlignCenter)
        dev_layout.addWidget(github_label)
        
        about_layout.addWidget(dev_card)
        
        about_layout.addStretch()
        
        # Copyright
        copyright_label = QLabel("© 2024 Vicky Dhale. All Rights Reserved.")
        copyright_label.setStyleSheet("color: #444444; font-size: 9px;")
        copyright_label.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(copyright_label)
        
        self.tabs.addTab(about_tab, "ℹ️ About")
        
        right_layout.addWidget(self.tabs)
        
        # Add to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([240, 960])
        main_layout.addWidget(splitter, 1)
        
        # CONSOLE
        console = QFrame()
        console.setFixedHeight(115)
        console.setObjectName("card")
        console_layout = QVBoxLayout(console)
        console_layout.setSpacing(2)
        console_layout.setContentsMargins(6, 4, 6, 4)
        
        console_header = QHBoxLayout()
        console_header.addWidget(QLabel("CONSOLE"))
        console_header.addStretch()
        
        btn_clear = QPushButton("Clear")
        btn_clear.setMaximumWidth(45)
        btn_clear.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #888888;
                border: none;
                font-size: 9pt;
                padding: 2px;
            }
            QPushButton:hover {
                color: #00a8e8;
            }
        """)
        btn_clear.clicked.connect(self.clear_console)
        console_header.addWidget(btn_clear)
        
        console_layout.addLayout(console_header)
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMaximumHeight(70)
        console_layout.addWidget(self.console)
        
        main_layout.addWidget(console)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("✓ Ready - Developed by Vicky Dhale")
        
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setMaximumWidth(100)
        self.status_bar.addPermanentWidget(self.progress)
        
        # Timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_status)
        self.refresh_timer.start(30000)
        
        # Initial data
        self.log("▶ Global License Manager started")
        self.log("✓ Developed by Vicky Dhale")
        self.update_system_info()
        self.refresh_status()
    
    def create_method_widget(self, title, description, method, primary=False):
        """Create method widget with ACTIVATE button"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 4px;
                padding: 6px;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setSpacing(2)
        layout.setContentsMargins(6, 6, 6, 6)
        
        # Title and button row
        row = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 11pt; font-weight: 600; color: {'white' if primary else '#00a8e8'};")
        row.addWidget(title_label)
        row.addStretch()
        
        btn = QPushButton("Activate")
        btn.setMaximumWidth(70)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #00a8e8;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 4px 8px;
                font-size: 8pt;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #0090c0;
            }
        """)
        btn.clicked.connect(lambda: self.start_activation(method))
        row.addWidget(btn)
        
        layout.addLayout(row)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #888888; font-size: 8pt;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        return widget
    
    def start_activation(self, method):
        """Start activation with dark popup"""
        if not ctypes.windll.shell32.IsUserAnAdmin():
            msg = DarkMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Admin Required")
            msg.setText("Administrator privileges required")
            msg.setInformativeText("Please run as Administrator for activation features.")
            msg.exec_()
            return
        
        # Dark confirmation dialog
        msg = DarkMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Confirm Activation")
        msg.setText(f"Start {method.value} activation?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        
        reply = msg.exec_()
        
        if reply == QMessageBox.Yes:
            self.progress.setVisible(True)
            self.progress.setValue(0)
            self.thread = ActivationThread(self.engine, method)
            self.thread.finished.connect(self.activation_finished)
            self.thread.progress.connect(self.progress.setValue)
            self.thread.log.connect(self.log)
            self.thread.start()
            self.status_bar.showMessage(f"⏳ Running {method.value}...")
    
    def activation_finished(self, success, message):
        self.progress.setVisible(False)
        icon = "✓" if success else "✗"
        self.status_bar.showMessage(f"{icon} {message}")
        self.recent_list.addItem(f"{icon} {message[:35]}...")
        self.log(f"{icon} {message}")
        self.refresh_status()
    
    def refresh_status(self):
        try:
            status = self.engine.get_status()
            display = "═" * 45 + "\n"
            display += "LICENSE STATUS\n"
            display += "═" * 45 + "\n\n"
            
            for key, value in status.items():
                display += f"  {key.replace('_', ' ').title()}: {value}\n"
            
            display += "\n" + "═" * 45 + "\n"
            display += f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            self.status_display.setText(display)
            self.status_bar.showMessage("✓ Status updated")
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
    
    def generate_report(self):
        try:
            report = self.engine.generate_report()
            self.report_display.setText(report)
            self.log("📊 Report generated")
            self.status_bar.showMessage("✓ Report generated")
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
    
    def save_report(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Report", 
            f"license_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text Files (*.txt)"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.report_display.toPlainText())
                self.log(f"💾 Report saved")
                QMessageBox.information(self, "Saved", f"Report saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
    
    def export_logs(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Logs",
            f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text Files (*.txt)"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.console.toPlainText())
                self.log("📤 Logs exported")
                QMessageBox.information(self, "Exported", f"Logs exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")
    
    def check_system(self):
        self.log("🔍 Checking system...")
        self.update_system_info()
        self.log("✓ System check completed")
    
    def save_settings(self):
        self.log("⚙️ Settings saved")
        msg = DarkMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Settings")
        msg.setText("Settings saved successfully!")
        msg.exec_()
    
    def show_docs(self):
        msg = DarkMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Documentation")
        msg.setText("Documentation available at:\nhttps://github.com/vickydhale/global-license-manager")
        msg.exec_()
    
    def show_about(self):
        self.tabs.setCurrentIndex(4)
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.append(f"[{timestamp}] {message}")
        cursor = self.console.textCursor()
        cursor.movePosition(cursor.End)
        self.console.setTextCursor(cursor)
    
    def clear_console(self):
        self.console.clear()
        self.log("📟 Console cleared")
    
    def update_system_info(self):
        try:
            import platform
            import winreg
            
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
            )
            build = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
            edition = winreg.QueryValueEx(key, "EditionID")[0]
            winreg.CloseKey(key)
            
            info = (f"OS: Windows 10\n"
                   f"Build: {build}\n"
                   f"Edition: {edition}\n"
                   f"Arch: {platform.machine()}")
            
            self.sys_info.setText(info)
        except Exception as e:
            self.sys_info.setText(f"System Info Unavailable")

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Global License Manager")
    app.setApplicationVersion("1.0.0")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()