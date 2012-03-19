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
 
# HTTPS connection

conn = httplib.HTTPSConnection(url)
conn.request("POST", "/v2.0/tokens", params, headers)

# response

response = conn.getresponse()
data = response.read()
dd = json.loads(data)

conn.close()

apitokenid = dd['access']['token']['id']
apitokentenantid = dd['access']['token']['tenant']['id']
apitokentenantname = dd['access']['token']['tenant']['name']

print "Your token ID is: %s" % apitokenid
print "Your token tenant ID is: %s" % apitokentenantid
print "Your token tenant name is: %s" % apitokentenantname

print json.dumps(dd, indent=2)

sc = dd['access']['serviceCatalog']
n = 0
m = range(len(sc))
foundNovaURL = False

for i in m:
	ss = sc[i]['name']
	#if ss == 'keystone':
	if ss == 'nova':
		#apiurl = sc[i]['endpoints'][0]['adminURL']
		apiurl = sc[i]['endpoints'][0]['publicURL']
		print "Your Nova URL: %s" % apiurl
		foundNovaURL = True

if foundNovaURL == False:
	print "No Nova URL found!"
	exit()

apiurlt = urlparse(apiurl)

params2 = urllib.urlencode({})
headers2 = { "X-Auth-Token":apitokenid, "Content-type":"application/json" }
conn2 = httplib.HTTPSConnection(apiurlt[1])
conn2.request("GET", "%s/images" % apiurlt[2], params2, headers2)

# HTTP response #2

response2 = conn2.getresponse()
data2 = response2.read()
print data2
dd2 = json.loads(data2)

print json.dumps(dd2, indent=2)

###
### Server parameters
###

# Server name

sname = "tornado001"

# Server image URL

n = len(dd2["images"])
m = range(n)

for i in m:
	if dd2["images"][i]["id"] == 1:
		sImageRef = dd2["images"][i]["links"][0]["href"]

###
### server metadata
###

sMetadata = {}

###
### server personalization
###

sPersonalityPath = ""
sPersonalityContents = ""
sPersonality = [ { "path":sPersonalityPath, "contents":base64.b64encode( sPersonalityContents ) } ]

sname = "server000"
sImageRef = 15
sFlavorRef = 1

s = { "server": { "name": sname, "imageRef": str(sImageRef), "flavorRef": str(sFlavorRef), "metadata": sMetadata, "personality": sPersonality } }

sj = json.dumps(s)

# HTTP connection #4

params4 = ""
headers4 = { "X-Auth-Token":apitokenid, "Content-type":"application/json" }

conn4 = httplib.HTTPSConnection(apiurlt[1])
conn4.request("GET", "%s/servers/1135/ips/internet" % apiurl, params4, headers4)

# HTTP response #4

response4 = conn4.getresponse()
data4 = response4.read()
dd4 = json.loads(data4)

conn4.close()

print json.dumps(dd4, indent=2)
