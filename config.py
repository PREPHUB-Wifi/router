# put constants here, probably port, etc. 
# use elsewhere as config.whatever

MLENGTH = 53 #DO NOT TOUCH

# run ports.py to see what this should be
#SERIALPORT = '/dev/ttyACM0'
SERIALPORT = '/dev/cu.usbmodem1411'

BAUD = 9600
PORT = 8000

HUB = 0

HOST = 'localhost'

# run ttl.py to see what this should be
MAX_TTL = 5

#format:
GRAPH = {'0': set(['1', '2']),
         '1': set(['0', '3', '4']),
         '2': set(['0', '5']),
         '3': set(['1']),
         '4': set(['2', '5']),
         '5': set(['2', '4'])}
