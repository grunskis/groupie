import json
import sys


payload_file = None
payload = None

for i in range(len(sys.argv)):
    if sys.argv[i] == "-payload" and (i + 1) < len(sys.argv):
        payload_file = sys.argv[i + 1]
        with open(payload_file, 'r') as f:
            payload = json.loads(f.read())


import urllib2

page = urllib2.urlopen(payload['url'])
page.read()
