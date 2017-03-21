#!/usr/bin/python3

# 1 Mile Radius Telephone is an interactive rotary telephone created for the 1 Mile Radius Project.
# Written by Jeffrey Dorfman, and using code from Ian Shelanskey and Simon Jenny.
# VERSION 1.1.1
# 19 March, 2017


import RPi.GPIO as GPIO  
import math, sys, os
import subprocess
import socket
import argparse
import random

from pythonosc import osc_message_builder
from pythonosc import udp_client

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Dial Circuit
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Release Dial Circuit
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Normally Open Reciever Switch

# ===== VARIABLES =====

c=0
last = 1
dialednum = 0

def count(pin):
	global c 
	c = c + 1
	
	
# ===== SETUP SCRIPT =====	


from subprocess import call
call(["amixer", "cset", "numid=1", "400"])
call(["amixer", "cset", "numid=3", "0"])
# Above adjusts volume of amixer to 100%, this line may vary depending on version. Use "amixer controls" to discover your numid=?
# Also ensures correct output, mine kept defaulting to the wrong one.

GPIO.add_event_detect(18, GPIO.BOTH)
GPIO.add_event_detect(24, GPIO.BOTH)

# ===== MAIN SCRIPT =====

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", default="10.1.10.18", help="The ip of the OSC server")
	parser.add_argument("--port", type=int, default=5005, help="The port the OSC server is listening on")
	args = parser.parse_args()

	client = udp_client.SimpleUDPClient(args.ip, args.port)
# Above is for OSC Protocols

while True:
	try:
		if GPIO.event_detected(18):
			
			try:
				player.kill()
			except NameError:
				pass
			
			current = GPIO.input(18)
			
			if(last != current):
				
					
				if(current == 0):
					GPIO.add_event_detect(23, GPIO.BOTH, callback=count, bouncetime=5)
	
				else:
					GPIO.remove_event_detect(23)
					number = math.floor(c/2.1)
					dialednum = str(number)
					player = subprocess.Popen(["mpg123", "/media/" + dialednum + ".mp3", "-q"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)	
					client.send_message(["/fire", random.random()) 
					c=0
					
				last = GPIO.input(18)
				
		if GPIO.event_detected(24):
			
			try:
				player.kill()
			except NameError:
				pass
			
	except KeyboardInterrupt:
		break
