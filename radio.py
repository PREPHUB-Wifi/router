import serial
import time
import config

class Radio:
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.ser = serial.Serial(port, baud)
        time.sleep(2) # give time to initialize
        self.sent = set()

    def listen(self):
        #print("listening...")
        return self.ser.readline()

    def send(self, packet):
        if packet[0] == "*": #broadcast
            if self.sent.contains(packet[1:5]):
                return #don't broadcast same packet twice
            self.sent.add(packet[1:5]) #ID and which -- uniquely identified packet
        print("radio is sending packet: ", packet.decode('utf-8'))
        self.ser.write(packet)

    def slice_message(self, message):
        return [message[i:i+config.MLENGTH] for i in \
            range(0, len(message), config.MLENGTH)]
