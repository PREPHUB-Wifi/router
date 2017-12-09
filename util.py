import config

def slice_message(message):
    ret = []
    for i in range(0, len(message), config.MLENGTH):
        ret.append(message[i:i+config.MLENGTH])
    return ret 

#takes in a string
#returns list of 64 byte packets, each packet is a byte obj
def encode(message, mid):
    returnlist = []
    mslices = slice_message(message)
    howmany = len(mslices)
    to = '*'
    mid = mid #message_json['pckt_id'] #midly redundant
    ttl = config.MAX_TTL
    for i in range(howmany):
        which = i + 1
        packet = encap(to, mid, which, howmany, ttl, mslices[i])
        returnlist.append(packet)

    return returnlist


#numbers, mslice is str 
def encap(to, mid, which, howmany, ttl, mslice):
    to = str(to)
    mid = str(mid) #str([0]*(6-len(mid))) + str(mid) #leading zeroes
    wh = str(which)
    hm = str(howmany)
    ttl = str(ttl)
    prefix = to + mid + wh + hm + ttl
    assert len(prefix) == 7
    #message = bytes(prefix, 'utf-8') + bytes(mslice, 'utf-8') + bytes('\n', 'utf-8')
    message = prefix + mslice + '\n'
    pad = 64- len(message)
    #message = message + bytes(' '*pad, 'utf-8')
    message = message + ' '*pad

    print(message)
    assert len(message) == 64
    return message

#decodes str pkt into a dictionary
def decode(pkt):
    stripped_data = pkt[7:].strip().replace('\n','')
    #pkt = pkt.decode('utf-8')
    return {"to":pkt[0], "mid":pkt[1:4], "which":pkt[4], "howmany":pkt[5], \
                        "ttl":pkt[6], "data":stripped_data}


