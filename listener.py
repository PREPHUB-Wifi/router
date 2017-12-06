from urllib.request import urlopen
from urllib.parse import urlencode  
import urllib.request
import http.client 
import time
from datetime import date
import config

def push_info(message):
	#data = parse apart info in json object 
	#make sure strings aren't empty
	data_encoded = urlencode(message)
	h = http.client.HTTPConnection('127.0.0.1:8081')
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	h.request('POST', '/notes', data_encoded, headers)
	r = h.getresponse()
	print(r.read())

# [to(1) : which(1) : howmany(1) : [to(1) : id(3) : data(58)]]
def parse(packet):
	#print(packet)
	text = packet.decode('utf-8')
	return {"to":text[0], "which":text[1], "howmany":text[2], \
		"ttl":text[3], "dest":text[4], "id":text[4:6], "data":text[4:]}


def listen_forever(radio):
	print("launched listener thread")
	while True:
		data = radio.listen()
		try:
			parsedict = parse(data)

			print("received: ", parsedict)
			print("pushing ", parsedict["data"], " to server")
			push_info(parsedict["data"])

			if parsedict["ttl"] > 0:
				#forward
				pass

		except:
			print("error decoding")
			print(data.decode('utf-8'))
			# probably half-sent garbage




