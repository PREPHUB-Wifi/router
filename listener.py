def push_info(packet):
	#data = parse apart info in json object 
	#make sure strings aren't empty
	data_encoded = urlencode(data)
	h = http.client.HTTPConnection('127.0.0.1:8081')
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	h.request('POST', '/notes', data_encoded, headers)
	r = h.getresponse()
	print(r.read())