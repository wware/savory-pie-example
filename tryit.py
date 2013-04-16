#!/usr/bin/python

"""
When we are doing runserver, we can test against the full stack.
"""

import urllib
import urllib2
import json
import pprint
import time
import os
import sys
import subprocess

opener = urllib2.build_opener(urllib2.HTTPHandler)

subprocess.Popen('./helper.sh')
time.sleep(2.5)

def get(url):
    request = urllib2.Request(url)
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'GET'
    data = json.load(opener.open(request))
    pprint.pprint(data)
    return data

def put(url, data):
    request = urllib2.Request(url, data=json.dumps(data))
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'PUT'
    opener.open(request)

def delete(url, data):
    request = urllib2.Request(url)
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'DELETE'
    opener.open(request)

try:
    data = get('http://localhost:8000/api/content')
    assert data['meta']['count'] == 2

    data = data['objects'][0]
    url = data['resourceUri']
    data['title'] = 'Harry Potter and the Endless Sequels'
    pprint.pprint(data)

    put(url, data)
    delete(url, data)

finally:
    for pid in os.popen('lsof -i:8000 | grep LISTEN | cut -c 8-12').read().strip().split('\n') + \
               os.popen('ps ax | grep helper.sh | cut -c 1-5').read().strip().split('\n'):
        if pid:
            try:
                os.kill(int(pid), 9)
            except OSError:
                pass
