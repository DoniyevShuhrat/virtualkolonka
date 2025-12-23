import sys
import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLabel, QComboBox, QPushButton, QTextEdit, QLineEdit
)


class ComPortApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Serial Port App")
        self.resize(600, 400)
        # self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Label
        label = QLabel("Available COM Ports:")
        layout.addWidget(label)

        # Dropdown (COM port list)
        self.combo = QComboBox()
        layout.addWidget(self.combo)

        # Button
        self.refresh_button = QPushButton("Refresh Ports")
        self.refresh_button.clicked.connect(self.refresh_ports)
        layout.addWidget(self.refresh_button)

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_port)
        layout.addWidget(self.connect_button)

        # Log window
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        # Container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.serial_port = None
        self.refresh_ports()

    def refresh_ports(self):
        """Detect available COM ports"""
        self.combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.combo.addItem(port.device)
        self.log.append("Ports refreshed.")

    def connect_port(self):
        """Connect to selected COM port"""
        port_name = self.combo.currentText()
        if not port_name:
            self.log.append("No port selected.")
            return

        try:
            self.serial_port = serial.Serial(port_name, 9600, timeout=1)
            self.log.append(f"Connected to {port_name}")
        except Exception as e:
            self.log.append(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ComPortApp()
    window.show()
    sys.exit(app.exec())
