#!/usr/bin/env python3
import traceback, sys
import urllib
import re
import json

from launchpadlib.launchpad import Launchpad

try:
    j = json.loads(sys.argv[1])
    if bool(j['launchpad-email']) == False:
        sys.exit(4)
    else:
        email = j['launchpad-email']

    l = Launchpad.login_anonymously(
        'ubuntu-community accomplishments', 'production')
    me = l.people.getByEmail(email=email)

    if me == None:
        sys.exit(1)
    else:
        username = str(me).split("~")[1]
        # we check the current planet config held in bzr for a LP username match
        url = "http://bazaar.launchpad.net/~planet-ubuntu/config/main/view/head:/config.ini"
        html_content = urllib.urlopen(url).read()
        matches = re.findall(username, html_content)

        if len(matches) == 0:
            sys.exit(1)
        else:
            sys.exit(0)

except SystemExit as e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)
