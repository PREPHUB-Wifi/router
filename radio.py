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
		print("listening...")
		return self.ser.readline()

	def send(self, message):
		print("radio is sending message: ", message)
		mslices = self.slice_message(message)
		howmany = len(mslices)
		to = message[0]
		nextdest = 0 #TODO
		for i in range(howmany):
			which = i + 1
			packet = self.encap(nextdest, which, howmany, mslices[i])
			print("radio is sending packet: ", packet.decode('utf-8'))
			self.ser.write(packet)

	def slice_message(self, message):
		return [message[i:i+config.MLENGTH] for i in \
			range(0, len(message), config.MLENGTH)]

	def encap(self, nextdest, which, howmany, mslice):
		dest = str(nextdest)
		wh = str(which)
		hm = str(howmany)
		prefix = dest + wh + hm
		message = bytes(prefix, 'utf-8') + mslice + bytes('\n', 'utf-8')
		assert len(message) <= 64
		return message

