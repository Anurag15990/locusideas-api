__author__ = 'Arvind'

import json, urllib2

node = "55afa9de50eb688360541439"

payload = {
    "node": node,
    "type": "user",
    "command":"update-work-focus",
    "data": {
        "work_focus":["color combination","furnishing","passage"]
    }
}


payload2 = {
    "node": node,
    "type": "user",
    "command":"update-work-style",
    "data": {
        "work_style":["vintage","modern","si-fi"]
    }
}

payload3 = {
    "node": node,
    "type": "user",
    "command":"update-work-interest",
    "data": {
        "work_interest":["offices","shops"]
    }
}


url = "http://localhost:4900/editors/invoke"

request = urllib2.Request(url)
request.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(request, json.dumps(payload))
response1 = urllib2.urlopen(request, json.dumps(payload2))
response2= urllib2.urlopen(request, json.dumps(payload3))

print str(json.load(response),"\n",json.load(response1),"\n",json.load(response2))