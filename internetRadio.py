#uses http requests to communicate instead of the serial port
#attribution to: https://docs.python.org/2/howto/sockets.html
import socket
import config

class Radio:
    def __init__(self, myPort, theirPort, hostname):
        self.myPort = myPort
        self.theirPort = theirPort
        self.hostname = hostname
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.csock = None
        if(myPort!=None):
            self.sock.bind(('0.0.0.0', self.myPort))
            self.sock.listen(10)

    def listen(self):
        if (self.csock == None): 
            #connecting for the first time 
            self.csock, caddr = self.sock.accept()
            print("internet radio accepted con:", caddr)
        chunks = []
        bytes_recd = 0
        while bytes_recd < 64:
            chunk = self.csock.recv(min(64 - bytes_recd, 2048))
            #print("internet radio got chunk!", chunk)
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)

        message = ''.join(str(chunks))
        print("internet radio got pkt:", message)
        return message

    #sends a single 64 byte pkt
    def send(self, pkt):
        #send a message to another InternetRadio class that is listening
        print("Sending to "+ self.hostname + ":" + str(self.theirPort))
        total_bytes_sent = 0
        self.sock.connect((self.hostname, self.theirPort))
        while total_bytes_sent < config.MLENGTH:
            sent = self.sock.send(pkt[total_bytes_sent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_bytes_sent += sent
        return

if __name__ == "__main__":
    radio = Radio(8001,8000, "")
    radio.listen()

