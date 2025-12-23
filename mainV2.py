import sys
import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QGroupBox, QFormLayout,
    QLabel, QComboBox, QPushButton, QTextEdit, QLineEdit
)

class ComPortApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VKolonka")
        self.resize(600, 400)
        # self.setGeometry(100, 100, 600, 400)

        vMainLayout = QVBoxLayout()
        hMainLayout = QHBoxLayout()
        vLayoutL = QVBoxLayout()
        vLayoutR = QVBoxLayout()
        hLayout1 = QHBoxLayout()

        # Dropdown (COM port list)
        labelComPort = QLabel("COM port:")
        hLayout1.addWidget(labelComPort)
        self.comboComPort = QComboBox()
        hLayout1.addWidget(self.comboComPort)

        # Dropdown (IP address list)
        labelIP = QLabel("IP address:")
        hLayout1.addWidget(labelIP)
        self.comboIP = QComboBox()
        hLayout1.addWidget(self.comboIP)

        vLayoutL.addLayout(hLayout1)


        dispenserConfData = QVBoxLayout()

        # """ ########################################### """
        # Dispenser configuration data / Dispenser setup data
        labelDispenser = QLabel("Установочные данные колонки")

        # Dispenser configuration data / Dispenser setup data
        groupSettings = QGroupBox("Установочные данные колонки")
        layoutSettings = QFormLayout()

        layoutSettings.addRow("Цена газа:", QLineEdit())
        layoutSettings.addRow("Приращение (м3):", QLineEdit())
        layoutSettings.addRow("Давление (кг/см2):", QLineEdit())
        layoutSettings.addRow("Всего (м3):", QLineEdit())

        groupSettings.setLayout(layoutSettings)
        vLayoutL.addWidget(groupSettings)

        # """ ########################################### """
        # Dispenser configuration data / Dispenser setup data
        groupProcess = QGroupBox("Ход заправки")
        layoutProcess = QFormLayout()

        layoutProcess.addRow("Заправлено (м3):", QLineEdit())
        layoutProcess.addRow("Сумма к оплате:", QLineEdit())

        groupProcess.setLayout(layoutProcess)
        vLayoutL.addWidget(groupProcess)

        # Button
        self.refresh_button = QPushButton("Refresh Ports")
        self.refresh_button.clicked.connect(self.refresh_ports)
        vLayoutL.addWidget(self.refresh_button)

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_port)
        vLayoutL.addWidget(self.connect_button)

        # """ Right Side """

        # Label
        label = QLabel("Monitors:")
        vLayoutR.addWidget(label)

        # Log window
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        vLayoutR.addWidget(self.log)

        vLayoutL.addStretch()
        # vLayoutR.addStretch()
        hMainLayout.addLayout(vLayoutL)
        hMainLayout.addLayout(vLayoutR)

        # MainVerticalLayout
        vMainLayout.addLayout(hMainLayout)

        # Container
        container = QWidget()
        container.setLayout(vMainLayout)
        self.setCentralWidget(container)

        self.serial_port = None
        self.refresh_ports()

        """-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==--=-=-"""

    def refresh_ports(self):
        """Detect available COM ports"""
        self.comboComPort.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.comboComPort.addItem(port.device)
        self.log.append("Ports refreshed.")

    def connect_port(self):
        """Connect to selected COM port"""
        port_name = self.comboComPort.currentText()
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
