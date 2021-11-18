#!/usr/bin/env python3
import traceback, sys
import json

import datetime
import requests
try:
    import json
except ImportError:
    import simplejson as json


from launchpadlib.launchpad import Launchpad

SERVICE_ROOT = 'http://summit.ubuntu.com/api'

class Summit(object):

    def __init__(self, service_root=None):
        self.service_root = service_root or SERVICE_ROOT
        self.cache = {}
        
    def clearCache(self, resource=None):
        if resource is None:
            self.cache = {}
        elif self.cache.has_key(resource):
            self.cache[resource] = {}
        
    # Generic, caching Collection
    def getCollection(self, resource, id_field='id', **kargs):
        if not self.cache.has_key(resource):
            self.cache[resource] = {}
        url = '/'.join([self.service_root, resource, ''])
        if len(kargs) > 0:
            url = '?'.join([url, requests.utils.quote(kargs)])
        s = requests.get(url)
        col = dict([(o[id_field], o) for o in json.load(s.text)])
        self.cache[resource].update(col)
        return col

    # Generic, cacheable Entity
    def getEntity(self, resource, entity_id):
        if not self.cache.has_key(resource):
            self.cache[resource] = {}
        if not self.cache[resource].has_key(entity_id):
            url = '/'.join([self.service_root, resource, str(entity_id)])
            s = requests.get(url)
            self.cache[resource][entity_id] = json.load(s.text)
        return self.cache[resource][entity_id]

try:
    j = json.loads(sys.argv[1])
    if bool(j['launchpad-email']) == False:
        sys.exit(2)
    else:
        email = j['launchpad-email']

    lp = Launchpad.login_anonymously(
        'ubuntu-community accomplishments', 'production')
    me = lp.people.getByEmail(email=email)
    if me is None:
        sys.exit(1)

    summit = Summit()
    attending = summit.getCollection('attendee', user__username=me.name, summit__date_start__lt=datetime.datetime.now().date())
    if len(attending) > 0:
        sys.exit(0)
    else:
        sys.exit(1)
    
except SystemExit as e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)
