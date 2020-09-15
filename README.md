# main

*meraki-WT-integrationBot*

---

## Motivation

This code is the reference to the "Program your network to work for you" webinar that was aired 16th of September 2020.  

main.py is the brain behind a Webex Teams bot that integrates with a Meraki Network. The goal of the bot is to outsource the taks of creating, deleting and managing SSID:s from a network engineer to the receptionst of the company. The whole value proposition is that the network engineer in this way offloads a repetitive and easy task to someone who does not necessarily come from an IT background. However, the code itself can be adjusted after your own needs (adjust functions, messages etc.) to whatever the purpose is. See it more as a framework/skeleton to get started with creating Webex Teams Bots, integrating with other systems and learning how to leverage APIs to do that. Enjoy ChatOps!! 

## Show Me!

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.


What visual, if shown, clearly articulates the impact of what you have created?  In as concise a visualization as possible (code sample, CLI output, animated GIF, or screenshot) show what your project makes possible.

## Features

Use a Webex Teams Bot in order to: 

- Create an SSID in a Meraki network
- Delete an SSID in a Meraki network
- Update an SSID in a Meraki network
- Maintain visibility for the network engineer in charge of the network. 

## Technologies & Frameworks Used

The application is built using a Flask framework and communicates with the help of Webhooks together with Webex Teams Cloud and the Meraki Dashboard. 

**Cisco Products & Services:**

- Cisco Meraki Cloud Managed Network
- Cisco Webex Teams Collaboration platform

**Tools & Frameworks:**

- Flask web application framework
- Webex Teams SDK
- Meraki SDK

## Pre-requisites

This application needs to be hosted somewhere where is has access to the internet. It can either be on your local machine where you use for instance a ngrok tunnel to access the internet, or you can host it on a PaaS. It is up to you.

## Installation

The first step is to clone this github repository in the directory where you will be running your code. 

```
git clone https://github.com/cskoglun/meraki-WT-integrationBot.git
```
The second step is to install all packages you need in order to run the code: 
```
pip install -r requirements.txt
```
Next thing you want to do is to update your environment variables that you store in a .env file. Never share these keys with anyone. The variables you need to store are: 

```
MERAKI_API_KEY=**PASTE_HERE**
GREG_BOT_TOKEN=**PASTE_HERE**
```
Next step is to fill out following variables: 

Which Meraki Network you want to communicate with: 
```
NETWORK_ID = "INSERT_NETWORK_ID" 
```

The Room ID of your Webex Teams Bot. You will find it at developer.webex.com under API Documentation and by using the API "GET Room List". 
```
ROOM_ID = "ROOM_ID"
```
## Authors & Maintainers

- Christina Skoglund <cskoglun@cisco.com>

## License

This project is licensed to you under the terms of the [Cisco Sample
Code License](./LICENSE).
