import serial
import threading

# portA = serial.Serial('COM4', 9600, timeout=0.1)
# portB = serial.Serial('COM5', 9600, timeout=0.1)

portA = serial.Serial('COM5', 9600, timeout=0.1)
portB = serial.Serial('COM7', 9600, timeout=0.1)

def forward(src, dst):
    while True:
        data = src.read(1024)
        if data:
            print(f"{src.port} → {dst.port}: {data}")
            dst.write(data)

threading.Thread(target=forward, args=(portA, portB), daemon=True).start()
threading.Thread(target=forward, args=(portB, portA), daemon=True).start()

input("Gateway running... Enter to quit.\n")