# put constants here, probably port, etc. 
# use elsewhere as config.whatever

MLENGTH = 53 #DO NOT TOUCH
#SERIALPORT = '/dev/ttyACM0'
SERIALPORT = '/dev/cu.usbmodem1411'

BAUD = 9600
PORT = 8000

HUB = 0

MAX_TTL = 5

#format:
GRAPH = {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['C', 'E'])}