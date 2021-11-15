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
    
  l=Launchpad.login_anonymously('ubuntu-community accomplishments',
                                'production')
  
  me=l.people.getByEmail(email=email)
  
  if me == None:
    sys.exit(1)
  
  try:
    mugshot = me.mugshot
    mugshot_handle = mugshot.open()
  except:
    sys.exit(1)
    
  sys.exit(0)

except SystemExit as e:
  sys.exit(e.code)
except:
  traceback.print_exc()
  sys.exit(2)

