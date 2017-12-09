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

    def listen(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', self.myPort))
        s.listen(1)
        csock, caddr = s.accept()
        chunks = []
        bytes_recd = 0
        while bytes_recd < config.MLENGTH:
            chunk = csock.recv(min(config.MLENGTH - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)

        message = ''.join(str(chunks))
        print(message)
        return message


    #sends a single 64 byte pkt
    def send(self, pkt):
        #send a message to another InternetRadio class that is listening
        self.sock.connect((hostname, theirPort))
        total_bytes_sent = 0
        while totalsent < config.MLENGTH:
            sent = self.sock.send(pkt[total_bytes_sent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_bytes_sent += sent
        return

if __name__ == "__main__":
    radio = InternetRadio(8001,8000, "")
    radio.listen()

