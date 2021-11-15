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

    # Get count of bugs reported by user from Launchpad, using email to
    # identify
    l = Launchpad.login_anonymously(
        'ubuntu-community accomplishments', 'production')
    me = l.people.getByEmail(email=email)
    if me == None:
        sys.exit(1)
    else:
        ubuntu=l.projects['ubuntu']
        bugs_reported = ubuntu.searchTasks(assignee=me, 
            status=['Fix Released'])
        if len(bugs_reported) > 0:
            sys.exit(0)
        else:
            sys.exit(1)

except SystemExit as e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)
