#!/usr/bin/python

import sys
import xmltodict
from elasticsearch import Elasticsearch
import requests
from datetime import datetime

#Yes, I still write in Python 2.7 until I'm forced not to.

if len(sys.argv) != 4:
	print 'Usage: vpn_users.py <firewall management IP> <API key> <Elasticsearch server>'
	sys.exit(0)
else:
	print 'Palo Alto IP: ' + sys.argv[1]
	print 'API key: ' + sys.argv[2]
	print 'Elasticsearch IP ' + sys.argv[3]

	pull_time = datetime.utcnow() 
	user_xml = requests.get('https://' + sys.argv[1] + '/api/?type=op&cmd=<show><global-protect-gateway><current-user/></global-protect-gateway></show>&key=' + sys.argv[2], verify=False)
	user_dict = xmltodict.parse(user_xml.text)
	es = Elasticsearch([{'host':'localhost','port':9200}])

	for item in user_dict['response']['result']['entry']:
		log_body = {'firewall':sys.argv[1],'pull-time':pull_time,'user':item['primary-username'],'os':item['client'],'login':item['login-time']}
		es.index(index='vpn_data',doc_type='vpn_user',body=log_body)
