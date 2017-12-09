from urllib.request import urlopen
from urllib.parse import urlencode  
import urllib.request
import http.client 
import time
from datetime import date
import config 
import accumulator 
import json


def push_info(message, host=config.HOST):
    #data = parse apart info in json object 
    #make sure strings aren't empty 

    #determine if Delete, put or post
    data_encoded = urlencode(message)
    h = http.client.HTTPConnection(host) #TODO config
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    h.request('POST', '/notes', data_encoded, headers)
    r = h.getresponse()
    print(r.read())


def parse(packet):
    #print(packet)
    #text = packet.decode('utf-8')
    text = packet
    print("I don't think it makes it past this line", packet)
    try:
        return {"to":text[0], "mid":text[1:4], "which":text[4], "howmany":text[5], \
            "ttl":text[6], "data":text[7:]}
    except IndexError:
        return {}


def listen_forever(radio):
    #TODO: reassemble packets
    print("launched listener thread") 
    a = accumulator.Accumulator()  
    message = None
    while True:
        packet = radio.listen()
        message = a.new(packet)
        if(message):
            handle_completed_message(message, radio)

def handle_completed_message(message, TXradio):  
    message_json = json.loads(message)
    s = json.dumps(message_json, indent=4, sort_keys=True) 

    # if parsedict["to"] == config.HUB or parsedict["to"] == "*":
    #     print("pushing ", parsedict["data"], " to server")
        #push_info(parsedict["data"])

    # if int(parsedict["ttl"]) > 0 and parsedict["to"] == "*":
    #     #forward
    #     packet = packet[0:6] + bytes([int(packet[6])-1]) + packet[7:] #decrement ttl
    #TXradio.send(s)
