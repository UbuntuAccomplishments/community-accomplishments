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

    l = Launchpad.login_anonymously('ubuntu-community accomplishments', 'production')
    me = l.people.getByEmail(email=email)
    if me == None:
        sys.exit(1)
    else:
        # Get user's launchpadID
        name = me.name

        # Get ubuntu-manual-tests project
        uca = l.projects['ubuntu-manual-tests']
        # Access it's trunk series
        ucatrunk = uca.getSeries(name='trunk')
        # Get trunk branch
        ucab = ucatrunk.branch
        # Look for all MP's that have been merged
        mps = ucab.getMergeProposals(status='Merged')

        for mp in mps:
            # If it was me who requested this merge...
            if mp.registrant.name == name:
                # Successful!
                sys.exit(0)

        # Merged MP's for this user were not found.
        sys.exit(1)

except SystemExit as e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)
