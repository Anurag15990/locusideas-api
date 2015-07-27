__author__ = 'neha'

import json, urllib2

node = "55b3e5485301fb1fea825909"
payload2 = {
    "node": node,
    "type": "user",
    "command": "update-contact-info",
    "data" : {
        "address" : "Chembur, Mumbai, Maharashtra - 400 089",
        "phone" : "23456789",
        "mobile" : "9886543210"
    }
}

url = "http://localhost:4900/editors/invoke"

request = urllib2.Request(url)
request.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(request, json.dumps(payload2))

print str(json.load(response))


