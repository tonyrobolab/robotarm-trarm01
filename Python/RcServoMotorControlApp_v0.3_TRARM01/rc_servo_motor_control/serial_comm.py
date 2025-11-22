# --------------------------------------------------------------------------------
#   File        serial_comm.py
#
#   Version     v0.1  2025.11.05  Tony Kwon
#                   Initial revision
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
#   Import
# --------------------------------------------------------------------------------
import serial

# --------------------------------------------------------------------------------
#   Class - SerialComm
# --------------------------------------------------------------------------------
class SerialComm:
    def __init__(self):
        self.ser = None

    def init(self, port, baud):
        try:
            self.ser = serial.Serial(port, baud, timeout=1)
            print('SerialComm init() OK')
            return True
        except:
            print('SerialComm init() NG')
            return False

    def deinit(self):
        try:
            self.ser.close()
            self.ser = None
        except:
            pass

    def write(self, data):
        self.ser.write(bytearray(data))

