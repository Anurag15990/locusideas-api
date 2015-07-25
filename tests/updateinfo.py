__author__ = 'neha'

import json, urllib2

node = "55b3e5485301fb1fea825909"
payload1 = {
    "node" : node,
    "type" : "user",
    "command" : "update-bio",
    "data" : {
        "bio" : "Hey there! I'm Anurag Agnihotri. I be so workaholic.. I skip meals to code. Coding > any other shiiiiiiit! #swag"
    }
}

payload2 = {
    "node" : node,
    "type" : "user",
    "command" : "update-institution",
    "data" : {
        "institution" : "Bharati Vidyapeeth College Of Engineering, Navi Mumbai. Jai Maharashtra!!"
    }
}

payload3 = {
    "node" : node,
    "type" : "user",
    "command" : "update-experience",
    "data" : {
        "experience" : "1.5 years - ILG, 1 year - Toovia"
    }
}

url = "http://localhost:4900/editors/invoke"

request = urllib2.Request(url)
request.add_header('Content-type', 'application/json')
response = urllib2.urlopen(request, json.dumps(payload3))

print str(json.load(response))