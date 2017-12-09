class Accumulator():
    def __init__(self):
        self.blobs = {} # maps message IDs to lists of dicts

    """
    Takes 64 byte raw packet, returns string containing full message if
    incoming packet is the last packet in the message, or None if it is 
    not. Message format: to(1), messageID(3), data
    """
    def new(self, packet):
        # parse the packet
        text = packet.decode('utf-8')
        packet_dict = {"to":text[0], "mid":text[1:7], "which":text[7], "howmany":text[8], \
            "ttl":text[9], "data":text[10:]}

        # either add to collection of packets for that message id or start new
        if packet_dict["mid"] in self.blobs.keys():
            blob = self.blobs[packet_dict["mid"]]
            blob.accept_new(packet_dict)
        else:
            blob = Blob(packet_dict)
            self.blobs[packet_dict["mid"]] = blob


        # check if that was the last packet we needed
        if blob.is_done():
            # build the message
            message = blob.build()
            # delete the blob
            del self.blobs[packet_dict["mid"]]
            return message
        else:
            return None

class Blob():
    """
    Assumes mid (message ID) of packet used for init does not already 
    correspond to a blob.
    """
    def __init__(self, packet_dict):
        self.packet_dict_dict = {int(packet_dict["which"]):packet_dict}
        self.mid = packet_dict["mid"]
        self.howmany = int(packet_dict["howmany"])

    def accept_new(self, packet_dict):
        self.packet_dict_dict[int(packet_dict["which"])] = packet_dict

    def is_done(self):
        return len(self.packet_dict_dict.keys()) == self.howmany

    def build(self):
        assert self.is_done()
        prefix = self.packet_dict_dict[1]["to"] + self.packet_dict_dict[1]["mid"]
        data = ""
        for i in range(1, self.howmany+1):
            data += self.packet_dict_dict[i]["data"]
        return prefix + data





