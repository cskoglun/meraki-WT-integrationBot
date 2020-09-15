#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""main Console Script.

Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""



__author__ = "Christina Skoglund"
__email__ = "cskoglun@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"








import requests
from flask import Flask, request
from webexteamssdk import WebexTeamsAPI, Webhook, webexteamssdkException
from meraki import DashboardAPI
from pprint import pprint
import os, json
from decouple import config



###################### These are variables and dictionaries and functions that are not to be changed. 

# Meraki Dashboard API information
# TODO Add MERAKI_API_KEY from your environment file .env
MERAKI_DASHBOARD_API_KEY = config("MERAKI_API_KEY") 
BASEURL = "https://api.meraki.com/api/v0/"

# The Meraki Network that Liza has access to
# TODO Add Network ID
NETWORK_ID = "INSERT_NETWORK_ID" 

# Headers for the REST API request
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": MERAKI_DASHBOARD_API_KEY
}

# Webex Teams information. Bot Token + Room ID
# TODO Add BOT_TOKEN from your environment file .env
BOT_TOKEN = config("BOT_TOKEN")
# TODO Add ROOM ID from your common ROOM with BOT
ROOM_ID = "ROOM_ID"

# Webex Teams SDK 
api = WebexTeamsAPI(access_token=BOT_TOKEN)

# Meraki SDK
dashboard = DashboardAPI(MERAKI_DASHBOARD_API_KEY)

###################### Frunctions in order to modularize the code

# Function: Get existing SSIDs for a network
def get_SSIDs_for_network():
    url = BASEURL + "networks/{}/ssids".format(NETWORK_ID)
    payload = None
    
    try: 
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()

        ssid_nr = ""
        ssid_name = ""
        ssid_nr_list = []
        ssid_name_list = []

        for item in response:
            if "Unconfigured SSID" in item["name"]:
                None
            else:
                ssid_nr = item["number"]
                ssid_name = item["name"]

                ssid_name_list.append(ssid_name)
                ssid_nr_list.append(ssid_nr)

    except Exception as e:
        print(f"ERROR get_SSIDs_for_network(): Requests status: {e}")


    return ssid_name_list, ssid_nr_list


# Create SSID for network
def create_ssid(name, password):

    # Automatically add number new number to new SSID
    getSSIDs = get_SSIDs_for_network()
    numbersSSID = len(getSSIDs[0])

    url = BASEURL + "networks/{}/ssids/{}".format(
        NETWORK_ID, numbersSSID
    )

    payload = {
        "name": name,
        "enabled": True,
        "authMode": "psk",
        "psk": password,
        "encryptionMode": "wpa",
        "wpaEncryptionMode": "WPA2 only",
    }
    payload = json.dumps(payload)
    try: 
        response = requests.request("PUT", url, headers=headers, data=payload)

    except requests.exceptions.ConnectionError as e:
        raise SystemExit(e)
    
    return response

# Delete SSID from network
def delete_ssid(name):
    SSIDs = get_SSIDs_for_network()
    if name in SSIDs[0]:
        index = SSIDs[0].index(name)
        number = SSIDs[1][index]

    displaynr = int(number) + 1
    url = BASEURL + "networks/{}/ssids/{}".format(
        NETWORK_ID, number
    )

    payload = {
        "name": "Unconfigured SSID {}".format(displaynr),
        "enabled": False,
        "authMode": "open",
    }
    payload = json.dumps(payload)

    try: 
        response = requests.request("PUT", url, headers=headers, data=payload)
    except requests.exceptions.ConnectionError as e:
        raise SystemExit(e)
    
    return response

# Help message
def help_me():
    
    return (
        "Sure! I can help. Below are the commands that I understand:\n"
        " Help - I will display my greeting message\n"
        "New SSID <name of new SSID> <password of new SSID> - Create new SSID (minimum 8 characters).\n"
        "Change password <SSID> <new password> - Manage SSID passwords \n"
        "Show - Show list of SSIDs.\n"
    )

# Generates string of all SSIDs in network
def show_ssids():
    ssid_list = get_SSIDs_for_network()
    string = ""
    for item in ssid_list[0]:
        string = string + "\n"+ item
    return string

## Flask application framework
app = Flask(__name__)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":

        json_data = request.json
        webhook_obj = Webhook(json_data)

        # Get the room details
        room = api.rooms.get(webhook_obj.data.roomId)
        # Get the message details
        message = api.messages.get(webhook_obj.data.id)
        # Get the sender's details
        person = api.people.get(message.personId)
        # Bot's information 
        me = api.people.me()

        if message.personId == me.id:
            # Message was sent by me (bot); do not respond.
            None

        else:
            text = message.text

            if "Help" in text or "help" in text:
                reply_text = str(help_me())
                markdown = help_me_markdown()
                api.messages.create(roomId=ROOM_ID, text=reply_text,markdown=markdown)

            elif "new" in text or "New" in text:
                textList = text.split()
                name_new_SSID = textList[len(textList) - 2]
                password_new_SSID = textList[len(textList) - 1]

                # If password is less than 8 characters, send error message.
                if len(password_new_SSID) < 8:

                    reply_text_m = (
                        "Oups! Password must be at **least 8 characters**. Please try again."
                    )
                    try:
                        api.messages.create(roomId=ROOM_ID,  markdown=reply_text_m)
                    except:
                        print("ERROR - could not create password warning message.")
                        pass
                else:
                    try:
                        
                        create_ssid(name_new_SSID, password_new_SSID)

                        # Message that is sent off to Liza's room

                        reply_text_markdown = "Thank you for your request, SSID **{}** has been created. Password: **{}**".format(
                            name_new_SSID, password_new_SSID
                        )
                        
                        # Message that is sent off to Greg's room 

                        reply_text_markdownc = "**FYI:** Liza created a new SSID: **{}** with password: **{}** at site: **Copenhagen**".format(
                            name_new_SSID, password_new_SSID
                        )
                        
                        api.messages.create(roomId=ROOM_ID,  markdown=reply_text_markdown)
                        tocommonroom= api.messages.create(roomId=ROOM_ID_commonRoom,  markdown=reply_text_markdownc)
                        
                    except:
                        print("ERROR - Message \"SSID created\" could not be created")
                        pass

            elif "delete" in text:
                textList = text.split()
                name_delete_SSID = textList[len(textList) - 1]

                if name_delete_SSID == "Merakilab.dk":
                    reply_text_m = "Unfortunately, {} is **not a SSID that you can delete** :( Contact Greg if you want it deleted.".format(name_delete_SSID)
                    try: 
                        api.messages.create(roomId=ROOM_ID, markdown=reply_text_m)
                    except:
                        print("ERROR: Could not create delete warning message")

                else: 
                    try:
                        delete_ssid(name_delete_SSID)
 
                        reply_text_m = (
                            "Thank you fror your request, **{}** has been deleted!".format(
                                name_delete_SSID
                            )
                        )

                        reply_text_markdownc = "**FYI:** Liza deleted SSID: **{}** at site: **Copenhagen**".format(
                            name_delete_SSID
                        )
                        
                        try:
                            api.messages.create(roomId=ROOM_ID, markdown=reply_text_m)
                            tocommonroom = api.messages.create(roomId=ROOM_ID_commonRoom,  markdown=reply_text_markdownc)
                        except: 
                              print("ERROR: Could not create delete success message")

                    except:
                        pass

            elif "Show" in text:
                try:
                    ssid_string = show_ssids()
                    reply_text = "Current SSIDs in network: " + ssid_string
                    api.messages.create(roomId=ROOM_ID, text=reply_text)
                except:
                    print("ERROR: Could not create Show message")
                    pass

            else:

                reply_text_m = (
                    "**Oups I did not understand :( I understand the following:**  \n"
                    "**Help** - I will display my greeting message  \n"  
                    "**New SSID** _NAME_SSID_ _PASSWORD_SSID_ - Create new SSID (minimum 8 characters).  \n"
                    "**Change password** _NAME_SSID_ _NEW_PASSWORD_SSID_ - Manage SSID passwords  \n"
                    "**Show** - Show list of SSIDs.  \n"
                )
                try:
                    api.messages.create(roomId=ROOM_ID, markdown=reply_text_m)
                except: 
                    print("ERROR: Could not create \"Cannot understand\" message. "


    return  "OK"

# Run application if this is main script
if __name__ == "__main__":
    app.debug = True
    app.run()
