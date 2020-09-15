# main

*meraki-WT-integrationBot*

---

## Motivation

This code is the reference to the "Program your network to work for you" webinar. 

main.py is the brain behind a Webex Teams bot that integrates with a Meraki Network. The goal of the bot is to outsource the taks of creating, deleting and managing SSID:s from a network engineer to the receptionst of the company. However, the code itself can be adjusted after your own needs (adjust functions, messages etc.). See it more as a framework to get started with creating Bots, integrating with other systems and learning how to leverage APIs to do that. Enjoy! 

## Show Me!

What visual, if shown, clearly articulates the impact of what you have created?  In as concise a visualization as possible (code sample, CLI output, animated GIF, or screenshot) show what your project makes possible.

## Features

Include a succinct summary of the features/capabilities of your project.

- Feature 1
- Feature 2
- Feature 3

## Technologies & Frameworks Used

This is Cisco Sample Code!  What Cisco and third-party technologies are you working with?  Are you using a coding framework or software stack?  A simple list will set the context for your project.

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

The first step is to clone this github repository to your directory. 

```
git clone https://github.com/cskoglun/meraki-WT-integrationBot.git
```
The second step is to install all packages you need in order to run the code: 
```
pip install -r requirements.txt
```
## Authors & Maintainers

- Christina Skoglund <cskoglun@cisco.com>

## License

This project is licensed to you under the terms of the [Cisco Sample
Code License](./LICENSE).
