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

    # Check if user has at least a valid ssh key
    # and at least a valid gpg key
    l = Launchpad.login_anonymously(
        'ubuntu-community accomplishments', 'production')
    me = l.people.getByEmail(email=email)
    if me == None:
        sys.exit(1)
    else:
        if len(me.sshkeys) > 0:
          sys.exit(0)
        sys.exit(1)

except SystemExit as e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)
