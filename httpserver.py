#https://gist.github.com/bradmontgomery/2219997

#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
from threading import Thread

import listener
import radio
import config 
import subprocess

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        content_length = int(self.headers['Content-Length'])
        message = self.rfile.read(content_length)
        data = JSON.dumps(message)
        if(data["no_sync"] == 1): 
            data_encoded = urlencode(data)
            h = http.client.HTTPConnection('127.0.0.1:8443')
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            h.request('POST', '/notes', data_encoded, headers)
            r = h.getresponse()
            print(r.read())
        else:
            #spawn sync, pass in the hash and 0/2
            pass

    def do_HEAD(self):
        #self._set_headers()
        pass
        
    def do_POST(self):
        #self._set_headers()
        #self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        content_length = int(self.headers['Content-Length'])
        message = self.rfile.read(content_length)
        print("radio is sending message: ", message)
        mslices = self.slice_message(message)
        howmany = len(mslices)
        to = message[0]
        nextdest = 0 #TODO
        for i in range(howmany):
            which = i + 1
            packet = self.encap(nextdest, which, howmany, mslices[i])
            radio.send(packet)

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

def run(server_class=HTTPServer, handler_class=S, port=config.PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Starting httpd...")
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv
    # init radio, start thread that handles incoming packets from radio
    radio = radio.Radio(config.SERIALPORT, config.BAUD)
    listener_thread = Thread(target = listener.listen_forever, args = (radio,))
    listener_thread.start()

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()