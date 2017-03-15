#!/usr/bin/python3
import RPi.GPIO as GPIO  
import math, sys, os
import subprocess
import socket

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

c=0
last = 1

def count(pin):
	global c 
	c = c + 1
	
from subprocess import call
call(["amixer", "cset", "numid=1", "400"])
call(["amixer", "cset", "numid=3", "0"])
"""
adjust volume of amixer to 100%, this line may vary depending on version. Use "amixer controls" to discover your numid=?
Also ensures correct output, mine kept defaulting to the wrong one.
"""

GPIO.add_event_detect(18, GPIO.BOTH)
GPIO.add_event_detect(24, GPIO.BOTH)

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
					if(waitforseconddial != 0):
						GPIO.add_event_detect(23, GPIO.BOTH, callback=count, bouncetime=300)
	
				else:
					GPIO.remove_event_detect(23)
					number = math.floor(c/2.1)
					player = subprocess.Popen(["mpg123", "/media/" + str(number) + ".mp3", "-q"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)	
					c=0
					
				last = GPIO.input(18)
				
		if GPIO.event_detected(24):
			
			try:
				player.kill()
			except NameError:
				pass
			
	except KeyboardInterrupt:
		break
