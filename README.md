Tool Timer
===================
web-based tool usage timer for maker space. server implemented in flask python web framework. Primarily intended to run on a raspberry pi with a relay board controlling the tool, it can also run on a pc with a USB Relay. It uses the flask web framework. It was inteded for the laser cutter at the Nova Labs Makerspace in Reston VA. 

## What it does
>- It asks the user for membership level (which determines pricing)
>- User Starts Tool, It keeps track of the time used
>- User Stops Tool. User can then click on a link which take them to their Nova Labs accounting page where they can make the payment

![](https://github.com/cogwheelcircuitworks/tool_timer/blob/master/doc/capture1.png "Logo Title Text 1")

![](https://github.com/cogwheelcircuitworks/tool_timer/blob/master/doc/raspi.gif "Logo Title Text 1")


## Raspi Installation Notes

>- Installed raspbian jessie 
>- sudo rpi-update; 
>- sudo apt-get update; 
>- (rebooted)
>- sudo apt-get upgrade;  # go get a coffee
>- https://www.raspberrypi.org/learning/python-web-server-with-flask/worksheet/
>- sudo apt-get python-pip
>- sudo pip install flask
>- sudo pip install flask-bootstrap

## Development Plan

>- Tool should use  **oAuth2** for authentication, prompting the user for their unique credentials
