# put constants here, probably port, etc. 
# use elsewhere as config.whatever

MLENGTH = 53 #DO NOT TOUCH

# run ports.py to see what this should be
#SERIALPORT = '/dev/ttyACM0'
SERIALPORT = '/dev/cu.usbmodem1411'

BAUD = 9600
PORT = 8000

HUB = 0

# run ttl.py to see what this should be
MAX_TTL = 5

#format:
GRAPH = {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['C', 'E'])}
