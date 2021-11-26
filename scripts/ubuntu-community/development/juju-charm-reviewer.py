#!/usr/bin/env python3
import traceback, sys
import json

# Add scripts/lib/ to the PYTHONPATH
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))
from helpers import Launchpad

try:
    j = json.loads(sys.argv[1])
    if not 'launchpad-email' in j or bool(j['launchpad-email']) == False:
        sys.exit(4)
    else:
        email = j['launchpad-email']
        
    me = Launchpad.fetch(email)
    if "charmers" in me.super_teams:
        sys.exit(0)
    else:
        sys.exit(1)

except SystemExit as e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)
