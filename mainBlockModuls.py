import sys
import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QComboBox, QPushButton,
    QTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox
)


class ComPortApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kolonka Controller")
        self.resize(850, 480)
        self.connectionStatus = False

        # ==== MAIN LAYOUT ====
        mainLayout = QHBoxLayout()

        # ==== LEFT SIDE PANEL ====
        leftLayout = QVBoxLayout()

        # ==== REFRESH_PORTS BUTTON ====
        self.btnRefresh = QPushButton("Обновить порты")
        self.btnRefresh.clicked.connect(self.refresh_ports)

        leftLayout.addWidget(self.btnRefresh)

        # Top wor (COM + IP)
        topRow = QHBoxLayout()
        topRow.addWidget(QLabel("Порт:"))
        self.comboComPort = QComboBox()
        topRow.addWidget(self.comboComPort)

        topRow.addWidget(QLabel("IP:"))
        self.comboIP = QComboBox()
        self.comboIP.addItems(["1", "2", "3", "4"])
        topRow.addWidget(self.comboIP)

        leftLayout.addLayout(topRow)

        # ==== GROUP 1: Setup ====
        groupSetup = QGroupBox("Установочные данные колонки")
        formSetup = QFormLayout()
        self.gasPrice = QLineEdit("2000")
        self.stepVolume = QLineEdit("0.01")
        self.gasPressure = QLineEdit("200")
        self.totalVolume = QLineEdit("1234560.79")

        formSetup.addRow("Цена газа:", self.gasPrice)
        formSetup.addRow("Приращение (м3):", self.stepVolume)
        formSetup.addRow("Давление (кг/см2):", self.gasPressure)
        formSetup.addRow("Всего (м3):", self.totalVolume)

        groupSetup.setLayout(formSetup)
        leftLayout.addWidget(groupSetup)

        # ==== GROUP 2: Filling Process ====
        groupProcess = QGroupBox("Ход заправки")
        formProcess = QFormLayout()
        self.filled = QLineEdit("0")
        self.cost = QLineEdit("0")
        formProcess.addRow("Заправлено (м3):", self.filled)
        formProcess.addRow("Сумма к оплате:", self.cost)
        groupProcess.setLayout(formProcess)
        leftLayout.addWidget(groupProcess)

        # ==== CONNECTION BUTTON ====
        self.btnConnect = QPushButton("Включить колонку")
        self.btnConnect.clicked.connect(self.connect_port)

        leftLayout.addWidget(self.btnConnect)

        # ==== START/STOP BUTTONS ====
        fuelStopLayout = QHBoxLayout()

        self.btnFueling = QPushButton("Пуск")
        self.btnStopFueling = QPushButton("Стоп")

        fuelStopLayout.addWidget(self.btnFueling)
        fuelStopLayout.addWidget(self.btnStopFueling)

        leftLayout.addLayout(fuelStopLayout)

        # ==== DEBUG BUTTON ====
        debugBtnLayout = QHBoxLayout()
        debugBtnLayout.addWidget(QLabel("DEBUG:"))

        self.btnSendData = QPushButton("Send")
        self.btnSendData.clicked.connect(self.send_data)

        self.debugText = QLineEdit()

        debugBtnLayout.addWidget(self.btnSendData)
        debugBtnLayout.addWidget(self.debugText)
        leftLayout.addLayout(debugBtnLayout)

        leftLayout.addStretch()

        # ==== RIGHT SIDE PANEL ====
        rightLayout = QVBoxLayout()

        groupLog = QGroupBox("Регистрация обмена:")
        logLayout = QVBoxLayout()
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        logLayout.addWidget(self.log)
        groupLog.setLayout(logLayout)

        rightLayout.addWidget(groupLog)

        # ==== CONNECTION BUTTONS ====
        btnsLayout = QHBoxLayout()

        self.btnSave = QPushButton("Сохранить")
        self.btnClear = QPushButton("Очистить")
        self.btnClear.clicked.connect(self.log.clear)
        self.btnExit = QPushButton("Выход")

        btnsLayout.addWidget(self.btnSave)
        btnsLayout.addWidget(self.btnClear)
        btnsLayout.addWidget(self.btnExit)

        rightLayout.addLayout(btnsLayout)

        # Combine sides
        mainLayout.addLayout(leftLayout, 1)
        mainLayout.addLayout(rightLayout, 2)

        # Apply to central widget
        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

        # Serial object
        self.refresh_ports()
        self.serial_port = None

        # STYLE
        self.apply_style()

    # ==== FUNCTIONS FOR STYLE ====

    def apply_style(self):
        self.setStyleSheet("""
        QGroupBox {
            font-weight: bold;
            border: 1px solid #888;
            border-radius: 6px;
            margin-top: 12px;
        }
        QGroupBox:title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 6px;
        }
        QLineEdit, QComboBox, QPushButton {
            padding: 4px;
            font-size: 14px;
        }
        QComboBox {
            width: 110%;
        }
        QTextEdit {
            font-size: 13px;
        }
        """)

        """-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==--=-=-"""

    def clear_log(self):
        self.log.clear()

    def refresh_ports(self):
        """Detect available COM ports"""
        self.comboComPort.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.comboComPort.addItem(port.device)
        self.log.append("Ports refreshed.")

    def is_connected(self):
        return self.serial_port is not None and self.serial_port.is_open

    def send_data(self):
        print("Send data")
        if self.serial_port and self.serial_port.isOpen():
            hex_str = self.debugText.text().strip()
            try:
                data = bytes.fromhex(hex_str)
                self.serial_port.write(data)
                self.log.append(f"Data sent > {hex_str}")
            except Exception as e:
                self.log.append(f"⚠ Hex format xato. {self.debugText.text()}")
        else:
            self.log.append("Сначала подключите колонку!")

    def connect_port(self):

        # Agar port hozirda ULANGAN bo'lsa → DISCONNECT qilamiz
        if self.serial_port and self.serial_port.isOpen():
            self.serial_port.close()
            self.serial_port = None
            self.log.append("Соединение закрыто.")
            self.btnConnect.setText("Включить колонку")  # Tugma nomini qaytarish
            return

        # Aks holda → CONNECT qilamiz
        """Connect to selected COM port"""
        port_name = self.comboComPort.currentText()
        if not port_name:
            self.log.append("Порт не выбран!")
            return

        if not port_name:
            self.log.append("No port selected.")
            return

        try:
            self.serial_port = serial.Serial(port_name, 9600, timeout=1)
            self.log.append(f"Подключено к {port_name}")
            self.btnConnect.setText("Отключить колонку")  # Tugma nomini o‘zgartiramiz
            self.connectionStatus = True
        except Exception as e:
            self.serial_port = None
            self.log.append(f"Ошибка подключения: {e}")
            # self.log.append(f"Error: {e}")
            self.connectionStatus = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ComPortApp()
    window.show()
    sys.exit(app.exec())
