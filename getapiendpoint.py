#!/usr/bin/python

import httplib
import json

##
## arguments
##

## make sure that url is set to the actual hostname/IP address,
## port number

url = "nova-api.trystack.org:5443"

## make sure that osuser is set to your actual username, "admin"
## works for test installs on virtual machines, but it's a hack

osuser = "userName"

## use something else than "shhh" for you password

ospassword = "userPassword"

params = '{"auth":{"passwordCredentials":{"username":"%s", "password":"%s"}}}' % (osuser, ospassword)

headers = {"Content-Type": "application/json"}
 
##
## HTTPS connection no. 1
##

conn = httplib.HTTPSConnection(url)
conn.request("POST", "/v2.0/tokens", params, headers)

##
## response
##

response = conn.getresponse()
data = response.read()
dd = json.loads(data)

conn.close()

apitokenid = dd['access']['token']['id']
apitokentenantid = dd['access']['token']['tenant']['id']
apitokentenantname = dd['access']['token']['tenant']['name']

print json.dumps(dd, indent=2)

print "Your token ID is: %s" % apitokenid
print "Your token tenant ID is: %s" % apitokentenantid
print "Your token tenant name is: %s" % apitokentenantname

sc = dd['access']['serviceCatalog']
n = 0
m = range(len(sc))

for i in m:
	ss = sc[i]['name']
	if ss == 'nova':
		apiurl = sc[i]['endpoints'][0]['publicURL']
		print "Your Nova URL: %s" % apiurl
		exit()

print "No Nova URL found!"
