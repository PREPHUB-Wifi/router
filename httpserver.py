#https://gist.github.com/bradmontgomery/2219997

#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
from threading import Thread
import json
import listener
import radio
import config
import internetRadio
import subprocess
import util


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        message = self.rfile.read(content_length)
        listener.parse_incoming_data(data)
        pass

    def do_HEAD(self):
        #self._set_headers()
        pass
        
    def do_POST(self):
        #self._set_headers()
        #self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        content_length = int(self.headers['Content-Length'])
        message = self.rfile.read(content_length)

        my_json = message.decode('utf8').replace("'", '"')
        message_json = json.loads(my_json)

        packets = util.encode(my_json, message_json['data']['pckt_id'])
        for each in packets:
            radio_TX.send(each)

        self.send_response(200, "{}")
        self.end_headers()
        return

def run(server_class=HTTPServer, handler_class=S, port=config.PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Starting httpd...")
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv
    # init radio, start thread that handles incoming packets from radio

    #radio_TX = internetRadio.Radio( None, 7000, 'elpis.mit.edu')
    radio_RX = internetRadio.Radio(7001, None ,'')
    listener_thread = Thread(target = listener.listen_forever, args = (radio_RX,))
    listener_thread.start()

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
