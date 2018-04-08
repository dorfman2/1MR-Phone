#!/usr/bin/python3

# 1MR-Phone Version 2.1 
# 24 March, 2018
# Written by Jeffrey Dorfman, with help from Aaron Sanderholm, based on code from Raaff (https://github.com/Raaff)
# 1 Mile Radius Telephone is an interactive rotary telephone created for the 1 Mile Radius Project.
# 
# 
#

# ===== Import Dependencies =====
import subprocess
import gpiozero
import math
import os, time
import argparse
import configparser


# ===== Global Variables =====
global start
start = True


# ===== Config.ini =====
config = configparser.ConfigParser()
config.read('config.ini')


# ===== Variables (called from config.ini)=====


# Your phone GPIO pins, using BCIM numbers
pin_rotaryenable = int(config.get('pin', 'rotaryenable')) #Clockwise Rotary Circuit
pin_countrotary = int(config.get('pin', 'countrotary'))   #Counter-clockwise Rotary Circuit
pin_hook = int(config.get('pin', 'hook'))                     #Hook or hangup Switch
    

# Bouncetimes
bouncetime_enable = float(config.get('bouncetime', 'enable'))
bouncetime_rotary = float(config.get('bouncetime', 'rotary'))
bouncetime_hook = float(config.get('bouncetime', 'hook'))


# ===== Class Definitions =====
class dial():
    
    def __init__(self, ip, port):
        self.pulses = 0
        self.number = ""
        self.counting = True
        self.calling = False


    def startcalling(self):
        self.calling = True
        self.player = subprocess.Popen(["mpg123", "-q", "/home/pi/1MR-Phone/media/dialtone.mp3", ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
            
            if self.number == "633": #If you dial "OFF" turns off Phone
                shutdown()
                return
            
            if self.number == "7867": #If you dial "STOP" exits python script, comment out once debugging is complete
                close()
                return
            
            elif os.path.isfile("/home/pi/1MR-Phone/media/" + self.number + ".mp3"):
                print("start player with number = %s" % self.number)
                
                try:
                    self.player.kill()
                    
                except:
                    pass
                
                self.player = subprocess.Popen(["mpg123", "/home/pi/1MR-Phone/media/" + self.number + ".mp3", "-q"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
        print("Stop counting. Got number %s.\n" % self.number)
        self.counting = False

    def addpulse(self):
        print("addpulse")
        if self.counting:
            print("real addpulse")
            self.pulses += 1

    def getnumber(self):
        return self.number

    def reset(self):
        print ("Hangup")
        self.pulses = 0
        self.number = ""
        try:
            self.player.kill()
            
        except:
            pass

def shutdown():
    subprocess.Popen(["sudo shutdown -h now"], shell=True)

def close():
    print("Phone has shutdown")
    exit(0)


# ===== Main Script =====
     
if __name__ == "__main__":
    
    rotaryenable = gpiozero.DigitalInputDevice(pin_rotaryenable, pull_up=True, bounce_time=bouncetime_enable)
    countrotary = gpiozero.DigitalInputDevice(pin_countrotary, pull_up=True, bounce_time=bouncetime_rotary)
    hook = gpiozero.DigitalInputDevice(pin_hook, pull_up=True, bounce_time=bouncetime_hook)
    parser = argparse.ArgumentParser()
    
    countrotary.when_deactivated = dial.addpulse
    countrotary.when_activated = dial.addpulse
    rotaryenable.when_activated = dial.startcounting
    rotaryenable.when_deactivated = dial.stopcounting
    hook.when_activated = dial.stopcalling
    hook.when_deactivated = dial.startcalling
    while True:
        time.sleep(1) 