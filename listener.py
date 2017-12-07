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
	h = http.client.HTTPConnection('127.0.0.1:8443') #TODO config
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	h.request('POST', '/notes', data_encoded, headers)
	r = h.getresponse()
	print(r.read())


def parse(packet):
	#print(packet)
	text = packet.decode('utf-8')
	try:
		return {"to":text[0], "mid":text[1:4], "which":text[4], "howmany":text[5], \
			"ttl":text[6], "data":text[7:]}
	except IndexError:
		return {}


def listen_forever(radio):
	#TODO: reassemble packets
	print("launched listener thread")
	while True:
		data = radio.listen()
		try:
			parsedict = parse(data)
			print("received: ", parsedict) 
			# note = dict() 
			# note[hash] = '0'
			# note[pckt_id] = parsedict[mid]
			# note[no_sync] = 0
			# note[newName] = parsedict[dest]
			# note[needHelp] = 'No'
			# note[notes] = parsedict[data]
			# note[time] = parsedict[howmany]
			# data_encoded = urlencode(parsedict)
			# h = http.client.HTTPConnection('127.0.0.1:8443')
			# headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
			# h.request('POST', '/notes', data_encoded, headers)
			print("received: ", parsedict)

			if parsedict["dest"] == config.HUB or parsedict["dest"] == "*":
				print("pushing ", parsedict["data"], " to server")
				push_info(parsedict["data"])

			if parsedict["ttl"] > 0 and parsedict["dest"] == "*":
				#forward
				parsedict["ttl"] -=1
				message = "" #TODO
				r = requests.post('127.0.0.1:'+config.PORT, data=message)

		except:
			print("error decoding")
			print(data.decode('utf-8'))
			# probably half-sent garbage




