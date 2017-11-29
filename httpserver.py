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
        # Doesn't do anything with posted data
        #self._set_headers()
        #self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        print("hi post")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        #format for radio.send - bytearray
        #can put radio in outer scope depending on how this is launched
        print(post_data)


def run(server_class=HTTPServer, handler_class=S, port=80, baud=9600):
    # init radio, start thread that handles incoming packets from radio
    radio = radio.radio(port, baud)
	listener_thread = Thread(target = listener.listen_forever(), args = (radio))
    thread.start()

    # start server
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Starting httpd...")
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()