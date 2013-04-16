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

USE_SUBPROCESS = (len(sys.argv) == 1)

if USE_SUBPROCESS:
    subprocess.Popen('./helper.sh')
    time.sleep(2.5)

def get(uri):
    request = urllib2.Request(uri)
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'GET'
    data = json.load(opener.open(request))
    return data

def put(uri, data):
    request = urllib2.Request(uri, data=json.dumps(data))
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'PUT'
    opener.open(request)

def post(uri, data):
    request = urllib2.Request(uri, data=json.dumps(data))
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'POST'
    opener.open(request)

def delete(uri):
    request = urllib2.Request(uri)
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'DELETE'
    opener.open(request)

REDIRECT_JSON = False
if REDIRECT_JSON:
    os.system('rm -f /tmp/junk.txt')
    outf = open('/tmp/junk.txt', 'w')

def show_all():
    data = {
        'content': get('http://localhost:8000/api/content'),
        'zone': get('http://localhost:8000/api/zone'),
        'zonecontent': get('http://localhost:8000/api/zonecontent'),
    }
    if REDIRECT_JSON:
        pprint.pprint(data, stream=outf)
        outf.write('\n' + (50 * '-') + '\n\n')
    else:
        pprint.pprint(data)
    return data


try:
    # Update then delete
    uri = 'http://localhost:8000/api/content/1'
    data = {
        'resourceUri': uri,
        'title': 'Harry Potter and the Endless Sequels',
        'zones': [{'name': 'abcd',
                   'resourceUri': 'http://localhost:8000/api/zone/1'}]
    }

    x = show_all()
    assert x['content']['meta']['count'] == 2
    assert x['zone']['meta']['count'] == 2
    assert x['zonecontent']['meta']['count'] == 2

    put(uri, data)
    x = show_all()
    assert x['content']['meta']['count'] == 2
    assert x['zone']['meta']['count'] == 2
    assert x['zonecontent']['meta']['count'] == 3

    delete(uri)
    x = show_all()
    assert x['content']['meta']['count'] == 1
    assert x['zone']['meta']['count'] == 2
    assert x['zonecontent']['meta']['count'] == 1

    # Create a new one then delete
    uri = 'http://localhost:8000/api/content'
    data = {
        'resourceUri': uri,
        'title': 'Another Dumb Title',
        'zones': [{'name': 'ijkl',
                   'resourceUri': 'http://localhost:8000/api/zone/1'}]
    }

    post(uri, data)
    x = show_all()
    assert x['content']['meta']['count'] == 2
    assert x['zone']['meta']['count'] == 2
    assert x['zonecontent']['meta']['count'] == 2

    delete('http://localhost:8000/api/content/3')
    x = show_all()
    assert x['content']['meta']['count'] == 1
    assert x['zone']['meta']['count'] == 2
    assert x['zonecontent']['meta']['count'] == 1

finally:
    if REDIRECT_JSON:
        outf.close()
    if USE_SUBPROCESS:
        for pid in os.popen('lsof -i:8000 | grep LISTEN | cut -c 8-12').read().strip().split('\n') + \
                   os.popen('ps ax | grep helper.sh | cut -c 1-5').read().strip().split('\n'):
            if pid:
                try:
                    os.kill(int(pid), 9)
                except OSError:
                    pass
