class Packet:
    STX = 0x01
    ETX = 0x03

    def __init__(self, device_id: bytes, cmd: int, data: bytes = b''):
        self.device_id = device_id  # b'01' -> 30 31
        self.cmd = cmd  # 0x02
        self.data = data  # payload

    def encode(self) -> bytes:
        frame = bytearray()
        frame.append(self.STX)
        frame.extend(self.device_id)
        frame.append(self.cmd)
        frame.append(self.data)
        frame.append(self.ETX)
        frame.append(self.calc_crc(frame))
        return bytes(frame)

    @staticmethod
    def decode(raw: bytes):
        if raw[0] != Packet.STX or raw[-2] != Packet.ETX:
            raise ValueError("Invalid frame")

        device_id = raw[1:3]
        cmd = raw[3]
        data = raw[4:-2]
        crc = raw[-1]

        pkt = Packet(device_id, cmd, data)
        return pkt

    @staticmethod
    def calc_crc(data: bytes):
        # XOR
        crc = 0
        for b in data:
            crc ^= b
        return crc
