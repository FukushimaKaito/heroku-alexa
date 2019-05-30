# coding: UTF-8

import urllib.request
import json

def createdata()
	url = "http://ambidata.io/api/v2/channels/10905/data?readKey=7e7df40858ef249c&n=1"

	req = urllib.request.Request(url)
	with urllib.request.urlopen(req) as res:
			ambdata = json.loads(res.read().decode('utf8'))
	return(ambdata)

