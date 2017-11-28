import serial
import time

class Radio:
	def __init__(self, port, baud):
		self.port = port
		self.baud = baud
		self.ser = serial.Serial(port, baud)
		time.sleep(2) # give time to initialize

	def listen(self):
		return self.ser.readline() #read(num) for bytes. timeout?

	def send(self, message):
		print "radio is sending: ", message
		self.ser.write(message)


if __name__ == "__main__":
	port = '/dev/cu.usbmodem1421'
	baud = 9600
	radio = Radio(port, baud)