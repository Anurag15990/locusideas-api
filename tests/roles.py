__author__ = 'neha'

import json, urllib2

node = "55b6897a50eb68635eb5dda9"
payload1 = {
    "node" : node,
    "type" : "user",
    "command" : "edit-role",
    "action" : "remove",
    "data" : {
        "role" : "Admin"
    }
}

url = "http://localhost:4900/editors/invoke"
request = urllib2.Request(url)
request.add_header('Content-type', 'application/json')
response = urllib2.urlopen(request, json.dumps(payload1))

print str(json.load(response))