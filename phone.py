#!/usr/bin/python3

import subprocess
import RPi.GPIO as GPIO
import math
import os, time


pin_rotaryenable = 18
pin_countrotary = 23
pin_hook = 24

bouncetime_enable = 0.01
bouncetime_rotary = 0.01
bouncetime_hook = 0.01

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
rotaryenable = GPIO.setup(pin_rotaryenable, GPIO.IN, pull_up=True, bounce_time=bouncetime_enable)
countrotary = GPIO.setup(pin_countrotary, GPIO.IN, pull_up=True, bounce_time=bouncetime_rotary)
hook = GPIO.setup(pin_hook, GPIO.IN, pull_up=True, bounce_time=bouncetime_hook)


def shutdown():
	subprocess.Popen(["tts", "shutting down now"])
	subprocess.Popen(["sudo", "shutdown", "-h", "now"])


class Dial():
	def __init__(self):
		self.pulses = 0
		self.number = ""
		self.counting = True
		self.calling = False

	def startcalling(self):
		self.calling = True
		self.player = subprocess.Popen(["mpg123", "/home/pi/rotarypi/mp3/dial.mp3", "-q"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	def stopcalling(self):
		self.calling = False
		self.reset()

	def startcounting(self):
		self.counting = self.calling

	def stopcounting(self):
		if self.calling:
			if self.pulses > 0:
				if math.floor(self.pulses / 2) == 10:
					self.number += "0"
				else:
					self.number += str(math.floor(self.pulses / 2))
			self.pulses = 0
			if self.number == "1178":
				shutdown()
			elif os.path.isfile("/home/pi/rotarypi/mp3/" + self.number + ".mp3"):
				print("start player with number = %s" % self.number)
				try:
					self.player.kill()
				except:
					pass
				
				self.player = subprocess.Popen(["mpg123", "/home/pi/rotarypi/mp3/" + self.number + ".mp3", "-q"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		self.counting = False

	def addpulse(self):
		print("addpulse")
		if self.counting:
			print("real addpulse")
			self.pulses += 1

	def getnumber(self):
		return self.number

	def reset(self):
		self.pulses = 0
		self.number = ""
		try:
			self.player.kill()
		except:
			pass


if __name__ == "__main__":
	
	dial = Dial()
	countrotary.when_deactivated = dial.addpulse
	countrotary.when_activated = dial.addpulse
	rotaryenable.when_activated = dial.startcounting
	rotaryenable.when_deactivated = dial.stopcounting
	hook.when_activated = dial.stopcalling
	hook.when_deactivated = dial.startcalling
	while True:
		time.sleep(1)
