import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Power Mode Switcher")
        self.setFixedSize(200, 150)

        # Create buttons
        self.power_save_btn = QPushButton("Power Save")
        self.performance_btn = QPushButton("Performance")
        self.balanced_btn = QPushButton("Balanced")
        self.get_mode_btn = QPushButton("Get Current Mode")

        # Connect button signals
        self.power_save_btn.clicked.connect(self.power_save_btn_clicked)
        self.performance_btn.clicked.connect(self.performance_btn_clicked)
        self.balanced_btn.clicked.connect(self.balanced_btn_clicked)
        self.get_mode_btn.clicked.connect(self.get_mode_btn_clicked)

        # Create layout and add buttons
        layout = QVBoxLayout()
        layout.addWidget(self.power_save_btn)
        layout.addWidget(self.performance_btn)
        layout.addWidget(self.balanced_btn)
        layout.addWidget(self.get_mode_btn)

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def power_save_btn_clicked(self):
        self.run_command("powerprofilesctl set power-saver", "Power Save Mode Activated")

    def performance_btn_clicked(self):
        self.run_command("powerprofilesctl set performance", "Performance Mode Activated")

    def balanced_btn_clicked(self):
        self.run_command("powerprofilesctl set balanced", "Balanced Mode Activated")

    def get_mode_btn_clicked(self):
        cmd_out = subprocess.run(["bash", "-c", "powerprofilesctl get"], capture_output=True, text=True)
        mode = cmd_out.stdout.strip()
        self.show_message("Current Mode", mode)

    def run_command(self, command, success_message):
        subprocess.run(["bash", "-c", command], capture_output=True, text=True)
        self.show_message("Success", success_message)

    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())