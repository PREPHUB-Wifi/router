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
		return self.ser.readline() #read(num) for bytes. timeout?

	def send(self, message):
		print "radio is sending: ", message
		mslices = slice_message(message)
		for mslice in mslices:
			#can do fancier stuff here
			packet = encap(mslice)
			self.ser.write(packet)

	def slice_message(self, message):
		return [message[i:i+config.MLENGTH] for i in \
			range(0, len(line), config.MLENGTH)]

	def encap(mslice):
		#TODO: bit twiddling


if __name__ == "__main__":
	port = '/dev/cu.usbmodem1421'
	baud = 9600
	radio = Radio(port, baud)