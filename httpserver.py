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
        print("MEEEESAGE in JSONNNN", message)
        my_json = message.decode('utf8').replace("'", '"')
        message_json = json.loads(my_json)

        s = json.dumps(message_json, indent=4, sort_keys=True) 
        print(s)
        try: 
            mslices = self.slice_message(message)
            howmany = len(mslices)
            to = '*'
            mid = message_json['pckt_id'] #midly redundant
            ttl = config.MAX_TTL
            print("radio is sending message: ", s)
            for i in range(howmany):
                which = i + 1
                packet = self.encap(to, mid, which, howmany, ttl, mslices[i])
                radio_TX.send(packet)
        
            self.send_response(200, "{}")
            self.end_headers()
            #self.wmessagefile.write()
            return
        except IndexError:
            pass

    def slice_message(self, message):
        return [message[i:i+config.MLENGTH] for i in \
            range(0, len(message), config.MLENGTH)]

    def encap(self, to, mid, which, howmany, ttl, mslice):
        to = str(to)
        mid = str(mid)
        wh = str(which)
        hm = str(howmany)
        ttl = str(ttl)
        prefix = to + mid + wh + hm + ttl
        message = bytes(prefix, 'utf-8') + mslice + bytes('\n', 'utf-8')
        
        print(message.decode('utf-8'))
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

    radio_TX = internetRadio.Radio( None, 7000,'' )
    radio_RX = internetRadio.Radio( 7001, None ,'' )
    listener_thread = Thread(target = listener.listen_forever, args = (radio_RX,))
    listener_thread.start()

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
