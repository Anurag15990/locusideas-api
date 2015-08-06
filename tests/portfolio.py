__author__ = 'neha'

import json, urllib2

portfolio = "55c360671925f36447bbae0f"

payload = {
    "type" : "creatives",
    "command" : "create-new-portfolio",
    "data" : {
        "title" : "Bits of Bombay",
        "owner" : "55b3e5485301fb1fea825909",
        "description" : "Images of the city that always moves.",
        "category" : ["Photography"],
        "sub-category" : ["Art Direction"],
        "tags" : ["Art", "Illustration", "Portrait", "Photo"]
    }
}

payload2 = {
    "node" : "55c360671925f36447bbae0f",
    "type" : "creatives",
    "command" : "update-portfolio",
    "data" : {
        "title" : "B.i.t.s of Bombay",
        "description" : "Changed data."
    }
}

payload3 = {
    "node" : portfolio,
    "type" : "creatives",
    "command" : "update-category",
    "action" : "add",
    "category" : "Architectural Photography"
}

payload4 = {
    "node" : portfolio,
    "type" : "creative",
    "command" : "update-sub-category",
    "action" : "add",
    "sub-category" : "Black and White Photography"
}

payload5 = {
    "node" : portfolio,
    "type" : "creatives",
    "command" : "update-tags",
    "action" : "remove",
    "tag" : "Illustration"
}



url = "http://localhost:4900/editors/invoke"

request = urllib2.Request(url)
request.add_header('Content-type', 'application/json')
response = urllib2.urlopen(request, json.dumps(payload2))

print str(json.load(response))
