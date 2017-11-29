from urllib.request import urlopen
from urllib.parse import urlencode  
import urllib.request
import http.client 
import time
from datetime import date
import config

def push_info(json_packet):
	#data = parse apart info in json object 
	#make sure strings aren't empty
	data_encoded = urlencode(json_packet)
	h = http.client.HTTPConnection('127.0.0.1:8081')
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	h.request('POST', '/notes', data_encoded, headers)
	r = h.getresponse()
	print(r.read())

# [to(1) : which(1) : howmany(1) : [to(1) : id(3) : data(58)]]
def parse(packet):



def listen_forever(radio):
	print("launched listener thread")
	while True:
		data = radio.listen()
		#insert parse logic etc here

		#default for testing:


