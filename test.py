import util
import json

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

if __name__ == "__main__":

