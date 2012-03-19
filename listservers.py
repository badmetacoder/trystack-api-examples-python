#!/usr/bin/python

import base64
import httplib
import json
import urllib
from urlparse import urlparse

# arguments

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
## response no. 1
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
foundNovaURL = False

for i in m:
	ss = sc[i]['name']
	if ss == 'nova':
		apiurl = sc[i]['endpoints'][0]['publicURL']
		print "Your Nova URL: %s" % apiurl
		foundNovaURL = True

if foundNovaURL == False:
	print "No Nova URL found!"
	exit()

apiurlt = urlparse(apiurl)

##
## HTTPS connection no. 2
##

params2 = urllib.urlencode({})
headers2 = { "X-Auth-Token":apitokenid, "Content-type":"application/json" }
conn2 = httplib.HTTPSConnection(apiurlt[1])
conn2.request("GET", "%s/servers" % apiurlt[2], params2, headers2)

##
## response no. 2
##

response2 = conn2.getresponse()
data2 = response2.read()
print data2
dd2 = json.loads(data2)

print json.dumps(dd2, indent=2)
