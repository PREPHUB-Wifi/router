import util
import json
import internetRadio

def test_encode_decode():
    rawData = '{"data":{"hash":"0","pckt_id":153,"no_sync":0,"newName":"tyuhig","needHelp":"hjhyujki","notes":"yhui","time":1512850659151},"operation":"POST"}'
    jsonFromServer = json.loads(rawData)

    mid = jsonFromServer['data']['pckt_id']
    print("mid", mid)
    packets = util.encode(rawData, 153)
    res = ''
    for each in packets:
        mes = util.decode(each)
        res = res + (mes['data'].strip())
        print(util.decode(each))

    res = res.replace('\n', '')
    print(res)
    assert rawData == res
    print(json.loads(res))

#do python3 http_server.py
def test_listen():
    radioTX = internetRadio.Radio(None, 7001, 'elpis.mit.edu')
    rawData = '{"data":{"hash":"0","pckt_id":153,"no_sync":0,"newName":"tyuhig","needHelp":"hjhyujki","notes":"yhui","time":1512850659151},"operation":"POST"}'
    jsonFromServer = json.loads(rawData)
    mid = jsonFromServer['data']['pckt_id']
    packets = util.encode(rawData, mid)
    for each in packets:
        radioTX.send(each)

if __name__ == "__main__":
    test_encode_decode()
    test_listen()

