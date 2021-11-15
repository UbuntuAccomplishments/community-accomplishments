#!/usr/bin/env python3
import traceback, sys
import json
import datetime

from launchpadlib.launchpad import Launchpad

# Add scripts/lib/ to the PYTHONPATH
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))
from helpers import LocoTeamPortal

GLOBAL_JAM_NAME = 'Global Jam'

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

    ltp = LocoTeamPortal()
    attending = ltp.getCollection('attendees', attendee_profile__user__username=me.name, promise="sure", team_event__date_begin__lt=datetime.datetime.now(), team_event__global_event__name__contains=GLOBAL_JAM_NAME)
    if len(attending) > 0:
        sys.exit(0)
    else:
        sys.exit(1)
    
except SystemExit as e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)
