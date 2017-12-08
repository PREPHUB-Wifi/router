import listener
import time

class Pulse():
    def __init__(self):
        self.lastmessage = None

    def update(self, message):
        if message[0] == '*': #broadcast packet
            self.lastmessage = message
        else: #sync packet
            self.lastmessage = None

    def send(self):
        if self.lastmessage != None:
            listener.push_info(self.lastmessage)

    def run_forever(self):
        while True:
            time.sleep(30)
            send()