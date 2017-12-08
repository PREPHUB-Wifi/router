import sys


def newly_received(incoming_hash):
    get_req = urllib.request.urlopen("http://localhost:8443/notes").read()
    get_data_json_format = json.loads(get_req.decode('utf-8')) 

    #get newest value from list server

    if(new_data["hash"] != get_data_json_format[0]["hash"]):
        to_send_list = []
        for d in get_data_json_format:
            d["no_sync"] = 1
            to_send_list.append(d)
            if(d["hash"] == new_data["hash"]): 
                data_encoded = urlencode(to_send_list)  #send missing packets to other prephub
                h = http.client.HTTPConnection('127.0.0.1:8000') #send via router
                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                h.request('POST', '/notes', data_encoded, headers)
                r = h.getresponse()
                print(r.read())
                break
        #send request to other prephub
        #tell them: my best hash is B and you gave me A, so I'll give you A give me everything in 
        #between A and B with no_sync = 2 

def send_missing_info(incoming_hash):
    get_req = urllib.request.urlopen("http://localhost:8443/notes").read()
    get_data_json_format = json.loads(get_req.decode('utf-8')) 

    to_send_list = []
    for d in get_data_json_format:
        if(d["hash"] == incoming_hash): 
            #send data 
            data_encoded = urlencode(to_send_list)  #send missing packets to other prephub
            h = http.client.HTTPConnection('127.0.0.1:8000') #send via router
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            h.request('POST', '/notes', data_encoded, headers)
            r = h.getresponse()
            print(r.read())
            break


if __name__ == '__main__':
    incoming_hash = sys.argv[1]
    sync = sys.argv[2]  
    if(sync == 0):
        newly_received(incoming_hash)
    else:
        send_missing_info(incoming_hash)

   
#else: 
   #get all data from server 
   #compare new packet to each data item
       #if we hit a match, then insert into that spot and replace server data with new list 
   #if we dont 
       #compute difference between most recent packet and top item in list 
       #get the different packets from the prpehub and stuff them into server
       #then add new item 




# def sync(is_initiator, in_queue, out_queue, mismatch_index, mismatch_hash):
#   # phase 0: initiate sync with other hub from index i
#   if isInitiator:
#       out_queue.put({sync: True, index: i, hashval: mismatch_hash, match: False})

#   # phase 1: search newest to oldest for last point hubs agree
#   last_good_index = -1
#   receiver_of_match = False
#   while True:
#       message = in_queue.get() # block here until other hub responds
#       if message[match]:
#           last_good_index = message.index
#           receiver_of_match = True
#           break
#       elif (message[hashval] == getHash(message[index]):
#           last_good_index = message[index]
#           out_queue.put({sync: True, index: message[index], \
#                   hashval: message[hashval], match: True, timestamp: None, timestamp: None})
#           break
#       else:
#           if message.index == 0: #hubs never agree:
#               #last_good_index remains -1
#               out_queue.put({sync: True, index: - 1, \
#                   hashval: defaul_hash, match: True})
#               break
#           else:
#               out_queue.put({sync: True, index: message[index] - 1, \
#                       hashval: getHash(message[index] - 1), match: False})

#   # TODO: think very carefully about whether race conditions can happen 
#   # during transition from phase 1 to phase 2, esp. re: bool control flags
#   # causing problems

#   # phase 2: having found divergence point, correct missing messages
#   if receiver_of_match: #this hub got match = True message
#       # initiate next phase
#       out_queue.put({sync: True, index: last_good_index + 1, \
#           hashval: getHash(last_good_index + 1), \
#           data: getData(last_good_index), end: False})

#   while True:
#       message = in_queue.get()
#       if message[end]:
#           break
#       their_data = message[data]
#       their_time = their_data.timestamp
#       index = message[index]
#       our_data = getData(index)
#       our_time = data.timestamp

#       (new_hashval, last_index) = datawrapper.add(their_data)
#       if new_hashval == mismatch_hash and last_index = mismatch_index:
#           # adding this packet brings us in sync with other hub
#           out_queue.put({end:True})
#           break
#       if their_time < our_time:
#           out_queue.put({sync: True, end: False, index: index + 1, \
#                   hashval: getHash(index + 1), data: getData(index + 1)})
#       elif their_time > our_time:
#           out_queue.put({sync: True, end: False, index: index, \
#                   hashval: getHash(index), data: getData(index)})
#       elif their_time == our_time:
#           if their_data == our_data:
#               # end up here if we hit > block but it's not the only error
#               # force index increment
#               # TODO: think carefully about this also
#               out_queue.put({sync: True, end: False, index: index + 1, \
#                   hashval: getHash(index + 1), data: getData(index + 1)})
#           else:
#               # rip