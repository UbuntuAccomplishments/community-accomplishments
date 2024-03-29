#!/usr/bin/env python3
import traceback, sys
import json
import requests
import json


try:
    j = json.loads(sys.argv[1])
    if bool(j["askubuntu-user-url"]) == False:
        sys.exit(1)
    else:
        userurl = j["askubuntu-user-url"]

    userid = int(userurl.split("/")[-2])
    print(userid)

    # API: https://api.stackexchange.com/docs/types/user
    try:
        user_req = requests.get('https://api.stackexchange.com/2.0/users/%d?site=askubuntu&key=zUuJiog6hjENJovHBpM11Q((' % userid)

    except:
        sys.exit(1)

    user_data = json.loads(user_req.text)
    user_type = user_data['items'][0]['user_type']

    if user_type == 'registered' or user_type == 'moderator':
        sys.exit(0)
    elif user_type == 'unregistered' or user_type == 'does_not_exist':
        sys.exit(1)
    else:
        print("A new user_type is in the StackExchange API, please report this as a bug and report the new user-type of %s for user %d" % (user_type, userid))
        sys.exit(1)

except SystemExit as e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)


