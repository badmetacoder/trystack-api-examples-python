#!/usr/bin/python

import base64
import httplib
import json
import urllib
from urlparse import urlparse

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
                break

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
conn2.request("GET", "%s/images" % apiurlt[2], params2, headers2)

##
## response no. 2
##

response2 = conn2.getresponse()
data2 = response2.read()
dd2 = json.loads(data2)
print json.dumps(dd2, indent=2)

###
### Server parameters
###

n = len(dd2["images"])
m = range(n)
simage = 'natty-server-cloudimg-amd64-kernel'

for i in m:
        if dd2["images"][i]["name"] == simage:
                sImageRef = dd2["images"][i]["id"]

##
## HTTPS connection no. 3
##

params3 = urllib.urlencode({})
headers3 = { "X-Auth-Token":apitokenid, "Content-type":"application/json" }
conn3 = httplib.HTTPSConnection(apiurlt[1])
conn3.request("GET", "%s/flavors" % apiurlt[2], params3, headers3)

##
## response no. 3
##

response3 = conn3.getresponse()
data3 = response3.read()
dd3 = json.loads(data3)

print json.dumps(dd3, indent=2)

n = len(dd3["flavors"])
m = range(n)
sflavor = 'm1.medium'

for i in m:
        if dd3["flavors"][i]["name"] == sflavor:
                sFlavorRef = dd3["flavors"][i]["id"]

###
### server metadata
###

sMetadata = {}

###
### server personalization
###

serverid = "1214"

s = { "resize": { "flavorRef": str(sFlavorRef) } }

sj = json.dumps(s)

##
## HTTPS connection no. 4
##

params4 = sj
headers4 = { "X-Auth-Token":apitokenid, "Content-type":"application/json" }

conn4 = httplib.HTTPSConnection(apiurlt[1])
conn4.request("POST", "%s/servers/%s/action" % (apiurl, serverid), params4, headers4)

##
## response no. 4
##

response4 = conn4.getresponse()
data4 = response4.read()

conn4.close()

print data4
