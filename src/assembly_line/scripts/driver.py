import socket
import time


class AssemblyLine:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self, index):
        if index not in [1, 2, 3, 4]: return

        try:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            data = b'\xFE\x05\x00\x00\x00\x00\xD9\xC5'
            if index == 2:
                data = b'\xFE\x05\x00\x01\x00\x00\x88\x05'
            elif index == 3:
                data = b'\xFE\x05\x00\x02\x00\x00\x78\x05'
            elif index == 4:
                data = b'\xFE\x05\x00\x03\x00\x00\x29\xC5'

            udp_socket.sendto(data, (self.host, self.port))
            udp_socket.close()
        except Exception as e:
            print e

    def stop(self, index):
        if index not in [1, 2, 3, 4]: return

        try:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            data = b'\xFE\x05\x00\x00\xFF\x00\x98\x35'
            if index == 2:
                data = b'\xFE\x05\x00\x01\xFF\x00\xC9\xF5'
            elif index == 3:
                data = b'\xFE\x05\x00\x02\xFF\x00\x39\xF5'
            elif index == 4:
                data = b'\xFE\x05\x00\x03\xFF\x00\x68\x35'

            udp_socket.sendto(data, (self.host, self.port))
            udp_socket.close()
        except Exception as e:
            print e

    def start_all(self):
        try:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            data = b'\xFE\x0F\x00\x00\x00\x04\x01\x00\x71\x92'
            udp_socket.sendto(data, (self.host, self.port))
            udp_socket.close()
        except Exception as e:
            print e

    def stop_all(self):
        try:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            data = b'\xFE\x0F\x00\x00\x00\x04\x01\xFF\x31\xD2'
            udp_socket.sendto(data, (self.host, self.port))
            udp_socket.close()
        except Exception as e:
            print e

    def get_ir_status(self):
        try:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.sendto(b'\xFE\x02\x00\x00\x00\x04\x6D\xC6', (self.host, self.port))
            result = udp_socket.recv(6)
            udp_socket.close()

            a = result[3] & 0x02 != 0
            b = result[3] & 0x04 != 0
            return a, b
        except Exception as e:
            print e
        return None