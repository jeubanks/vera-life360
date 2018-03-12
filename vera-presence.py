#!/usr/bin/env python3
"""
Requirements:
 - Python3
 - Life360 user account
 - People setup in Life360
 - "Home" Geofence location defined in Life360

Setup:
Line 28: Life360 Username/email/phone number
Line 29: Life360 password

By default the Vera virtual switch name is the first name of the Life360 user.

Example:
Vera Vswitch: John
Life360 user: John

If they match everything works.  If they don't match an if/else needs to be put into place.
If have this in my setup, but I didn't know if others would need it.  If wanted open
and issue and I'll include by default

Uncoment lines 30 - 35 for basic debugging or to get your device names if unsure

Usage:
1. Install Virtual Switch plugin for Vera.  Availabe in the app store
2. Create a virtual switch for each Life360 user you want to check
3. Home geofence location MUST be setup
4. Run script from a system with Python3.  I recommend setting up a cronjob or similar
"""

from life360 import life360
import requests
import time
import vera

if __name__ == "__main__":
    # Local connection using IP address on local network.
    ve = vera.VeraLocal("<YOUR_VERA_LOCAL_IP")

    # Debugging get a list of devices
    # for i in ve.get_devices():
    #     if i.room != None:
    #         room = i.room.name
    #     else:
    #         room = "n/a"
    #     print("  %s: %s (%s)" % (i.id, i.name, room))

    # basic authorization hash (base64 if you want to decode it and see the sekrets)
    # this is a googleable or sniffable value. i imagine life360 changes this sometimes. 
    authorization_token = "cFJFcXVnYWJSZXRyZTRFc3RldGhlcnVmcmVQdW1hbUV4dWNyRUh1YzptM2ZydXBSZXRSZXN3ZXJFQ2hBUHJFOTZxYWtFZHI0Vg=="
    
    # your username and password (hope they are secure!)
    username = "<YOUR_USERNAME>"
    password = "<YOUR_PASSWORD>"

    #instantiate the API
    api = life360(authorization_token=authorization_token, username=username, password=password)
    if api.authenticate():

        #Grab some circles returns json
        circles =  api.get_circles()
        
        #grab id
        id = circles[0]['id']

        #Let's get your circle!
        circle = api.get_circle(id)

        #Let's display some goodies
        # print("Circle name:", circle['name'])
        # print("Members (" + circle['memberCount'] + "):")

        for m in circle['members']:
            # print("\tName:", m['firstName'],m['lastName'])
            # print("\tLocation:" , m['location']['name'])
            
            firstname = str (m['firstName'])
            place = str (m['location']['name'])
            
            dev = ve.get_device(firstname)
            if place == "Home":
                dev.set_vswitch(True)
            else:
                dev.set_vswitch(False)
    else:
        print("Error authenticating")  
