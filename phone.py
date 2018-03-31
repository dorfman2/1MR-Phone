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
from pythonosc import udp_client


# ===== Global Variables =====
global client
global start

start = True


# ===== Config.ini =====
config = configparser.ConfigParser()
config.read('config.ini')


# ===== Variables (called from config.ini)=====

# What ip & port number OSC sends to.
osc_ip = config.get('osc', 'ip')
osc_port = int(config.get('osc', 'port'))


# Your phone GPIO pins, using BCIM numbers
pin_rotaryenable = int(config.get('pin', 'rotaryenable')) #Clockwise Rotary Circuit
pin_countrotary = int(config.get('pin', 'countrotary'))   #Counter-clockwise Rotary Circuit
pin_hook = int(config.get('pin', 'hook'))                     #Hook or hangup Switch
    

# Bouncetimes
bouncetime_enable = int(config.get('bouncetime', 'enable'))
bouncetime_rotary = int(config.get('bouncetime', 'rotary'))
bouncetime_hook = int(config.get('bouncetime', 'hook'))


# ===== Test for Network =====    
def connect(ip, port):
     try:
         client = udp_client.SimpleUDPClient(ip, port)
     except OSError as err:
         print("OS error: {0}".format(err))
         print("woot")
         exit(1)
     return client
#     cfg = configparser.ConfigParser()
#     cfg.read("config.ini")
#     sections = cfg.sections()
#     api_key = cfg.get('section', 'api_key')
#     print(api_key)


# ===== Class Definitions =====
class Dial():
    def __init__(self, client):
        self.pulses = 0
        self.number = ""
        self.counting = True
        self.calling = False
        self.client = client

    def startcalling(self):
        self.calling = True
        self.client.send_message("cue/dialling", 1)
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
                self.client.send_message("Phone has entered Shutdown", 1)
                shutdown()
                return
            
            if self.number == "7867": #If you dial "STOP" exits python script, comment out once debugging is complete
                self.client.send_message("Phone has closed program, please restart to enable", 1)
                close()
                return
            
            elif os.path.isfile("/home/pi/1MR-Phone/media/" + self.number + ".mp3"):
                print("start player with number = %s" % self.number)
                
                try:
                    self.player.kill()
                    
                except:
                    pass
                
                self.client.send_message("cue/" + self.number + "/fire", self.number)
                self.player = subprocess.Popen(["mpg123", "/home/pi/1MR-Phone/media/" + self.number + ".mp3", "-q"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
        self.client.send_message("cue/hangup", 1)
        self.pulses = 0
        self.number = ""
        try:
            self.player.kill()
            
        except:
            pass


# OSC Class - possibly pull out 
class OSC():
    def __init__(self, client):



# ===== Main Script =====
def main():

    # Define Pins
    rotaryenable = gpiozero.DigitalInputDevice(pin_rotaryenable, pull_up=True, bounce_time=bouncetime_enable)
    countrotary = gpiozero.DigitalInputDevice(pin_countrotary, pull_up=True, bounce_time=bouncetime_rotary)
    hook = gpiozero.DigitalInputDevice(pin_hook, pull_up=True, bounce_time=bouncetime_hook)
    parser = argparse.ArgumentParser()
    
    # Configure OSC
    parser.add_argument("--ip", default=osc_ip, help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=osc_port, help="The port the OSC server is listening on")
    args = parser.parse_args() 
    client = connect(args.ip, args.port)
    
    
    
    
    
    
    dial = Dial(client)
    countrotary.when_deactivated = dial.addpulse
    countrotary.when_activated = dial.addpulse
    rotaryenable.when_activated = dial.startcounting
    rotaryenable.when_deactivated = dial.stopcounting
    hook.when_activated = dial.stopcalling
    hook.when_deactivated = dial.startcalling
    while True:
        time.sleep(1)
        

def shutdown():
    subprocess.Popen(["sudo shutdown -h now"], shell=True)

def close():
    exit(0)
        
if __name__ == "__main__":
    main()    
    if (start == 1):
        start = 0
        print("Phone On")
        client.send_message("Startup Complete", 1) 
