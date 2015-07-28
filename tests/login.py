__author__ = 'anurag'

import urllib2,json

payload1 = {
    "type" : "user",
    "command" : "login",
    "data" : {
        "email" : "anurag.agnihotri@ensuantinc.com",
        "password": "27572812"
    }
}

url = "http://localhost:4900/editors/invoke"

request = urllib2.Request(url)
request.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(request, json.dumps(payload1))

print str(json.load(response))