#!/usr/bin/python3

# 1 Mile Radius Telephone is an interactive rotary telephone created for the 1 Mile Radius Project.
# Written by Jeffrey Dorfman, and using code from Ian Shelanskey and Simon Jenny.
# VERSION 1.1.2
# 29 March, 2017


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
reciever = 0 # 0 is pressed, 1 is released
startup = 0

def count(pin):
	global c 
	c = c + 1
	
	
# ===== SETUP SCRIPT =====	


from subprocess import call
call(["amixer", "cset", "numid=1", "400"])
call(["amixer", "cset", "numid=3", "0"])
# Above adjusts volume of amixer to 100%, this line may vary depending on version. Use "amixer controls" to discover your numid=?
# Also ensures correct output, mine kept defaulting to the wrong one.

# ===== MAIN SCRIPT =====

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", default="192.168.1.220", help="The ip of the OSC server")
	parser.add_argument("--port", type=int, default=8000, help="The port the OSC server is listening on")
	args = parser.parse_args()

	client = udp_client.SimpleUDPClient(args.ip, args.port)
# Above is for OSC Protocols


GPIO.add_event_detect(18, GPIO.BOTH)
GPIO.add_event_detect(24, GPIO.BOTH)

reciever = GPIO.input(24)

# Above is to set GPIO Pins

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
					player = subprocess.Popen(["mpg123", "-q", "-@", "/media/" + dialednum + ".m3u"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					client.send_message("cue/" + dialednum + "/fire", dialednum)
					c=0
					
				last = GPIO.input(18)
				
		if GPIO.event_detected(24):
			reciever = GPIO.input(24)
			if(startup == 0):
				player = subprocess.Popen(["mpg123", "-q", "/media/dialtone.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				startup = 1
			if(reciever == 0):
				try:
					player.kill()
					client.send_message("cue/hangup", 0)
				except NameError:
					pass

			if(reciever == 1):
		
				try:
					player.kill()
					player = subprocess.Popen(["mpg123", "-q", "/media/dialtone.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					client.send_message("cue/dialtone", 0)
				except NameError:
					pass
			
		
	except KeyboardInterrupt:
		break
