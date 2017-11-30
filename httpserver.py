#https://gist.github.com/bradmontgomery/2219997

#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
from threading import Thread

import listener
import radio
import config

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        #self._set_headers()
        #self.wfile.write("<html><body><h1>hi!</h1></body></html>")
        print("hi get")

    def do_HEAD(self):
        #self._set_headers()
        print("hi head")
        
    def do_POST(self):
        #self._set_headers()
        #self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        print("hi post")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        radio.send(post_data)
        print(post_data)


def run(server_class=HTTPServer, handler_class=S, port=80):
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