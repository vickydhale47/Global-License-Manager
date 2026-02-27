from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt5.QtGui import QFont


class CyberSplashScreen(QWidget):

    def __init__(self):
        super().__init__()

        self.setFixedSize(700, 420)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.progress_value = 0
        self.init_ui()
        self.fade_in()
        self.start_loading()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("GLOBAL LICENSE MANAGER")
        title.setFont(QFont("Consolas", 26, QFont.Bold))
        title.setStyleSheet("color: #00a8e8;")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Professional Edition")
        subtitle.setFont(QFont("Consolas", 12))
        subtitle.setStyleSheet("color: #00ffff;")
        subtitle.setAlignment(Qt.AlignCenter)

        dev = QLabel("Developed by VICKY DHALE")
        dev.setFont(QFont("Consolas", 10))
        dev.setStyleSheet("color: #888888;")
        dev.setAlignment(Qt.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setFixedWidth(500)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00a8e8;
                border-radius: 8px;
                background-color: #0a0a0a;
                color: #00ffff;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #00a8e8;
                border-radius: 8px;
            }
        """)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(dev)
        layout.addSpacing(20)
        layout.addWidget(self.progress)
        layout.addStretch()

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #0a0a0a;
                border: 2px solid #00a8e8;
                border-radius: 15px;
            }
        """)

    def fade_in(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(1000)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

    def start_loading(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(30)

    def update_progress(self):
        self.progress_value += 1
        self.progress.setValue(self.progress_value)

        if self.progress_value >= 100:
            self.timer.stop()
            self.launch_main()

    def launch_main(self):
        from .main_window import MainWindow
        self.main = MainWindow()
        self.main.show()
        self.close()