import serial
import time
import config

class Radio:
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.ser = serial.Serial(port, baud)
        time.sleep(2) # give time to initialize

    def listen(self):
        #print("listening...")
        return self.ser.readline()

    def send(self, packet):
        print("radio is sending packet: ", packet.decode('utf-8'))
        self.ser.write(packet)

    def slice_message(self, message):
        return [message[i:i+config.MLENGTH] for i in \
            range(0, len(message), config.MLENGTH)]
