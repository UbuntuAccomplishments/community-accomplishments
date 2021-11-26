#!/usr/bin/env python3
import traceback, sys
import json

from launchpadlib.launchpad import Launchpad

try:
    j = json.loads(sys.argv[1])
    if not 'launchpad-email' in j or bool(j['launchpad-email']) == False:
        sys.exit(4)
    else:
        email = j['launchpad-email']


    l = Launchpad.login_anonymously(
        'ubuntu-community accomplishments', 'production')
    me = l.people.getByEmail(email=email)
    if me == None:
        sys.exit(1)
    else:
        sys.exit(0)

except SystemExit as e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)
