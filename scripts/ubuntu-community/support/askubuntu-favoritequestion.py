#!/usr/bin/env python3
import traceback, sys
import json


# Add scripts/lib/ to the PYTHONPATH
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))
from helpers import AskUbuntu

try:
    j = json.loads(sys.argv[1])
    if bool(j["askubuntu-user-url"]) == False:
        sys.exit(4)
    else:
        userurl = j["askubuntu-user-url"]

    userid = int(userurl.split("/")[-2])
    badgeid = 33

    me = AskUbuntu.fetch(userid)
    if badgeid in me.badges:
        sys.exit(0)
    else:
        sys.exit(1)

except SystemExit as e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)
