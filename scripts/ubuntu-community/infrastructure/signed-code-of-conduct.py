#!/usr/bin/env python3
import traceback, sys
import json

from launchpadlib.launchpad import Launchpad

try:
    j = json.loads(sys.argv[1])
    if bool(j['launchpad-email']) == False:
        sys.exit(4)
    else:
        email = j['launchpad-email']
    lp = Launchpad.login_anonymously(
        'ubuntu-community accomplishments', 'production')
    me = lp.people.getByEmail(email=email)
    if me == None:
        sys.exit(1)
    else:
        if me.is_ubuntu_coc_signer == True:
            sys.exit(0)
        else:
            sys.exit(1)

except SystemExit as e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)
