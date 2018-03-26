#!/usr/bin/python3

# 1 Mile Radius Telephone is an interactive rotary telephone created for the 1 Mile Radius Project.
# Version 2.1, written by Jeffrey Dorfman & Aaron Sanderholm, using code from Raaff (https://github.com/Raaff)
# 24 March, 2018

import subprocess
import gpiozero
import math
import os, time
import argparse
import configparser
from pythonosc import udp_client

global start
start = True

config = configparser.ConfigParser()
config.read('config.ini')
# ===== Variables =====

# What ip & port number OSC sends to.

osc_ip = config['osc']['ip']
osc_port = int(config['osc']['port'])

# Your phone GPIO pins, using BCIM numbers
pin_rotaryenable = int(config['pin']['rotaryenable']) #Clockwise Rotary Circuit
pin_countrotary = int(config['pin']['countrotary'])   #Counter-clockwise Rotary Circuit
pin_hook = int(config['pin']['hook'])                 #Hook or hangup Switch
    
bouncetime_enable = int(config['bouncetime']['enable'])
bouncetime_rotary = int(config['bouncetime']['rotary'])
bouncetime_hook = int(config['bouncetime']['hook'])
    
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
        
# ===== Main Script =====
            
def main():


    rotaryenable = gpiozero.DigitalInputDevice(pin_rotaryenable, pull_up=True, bounce_time=bouncetime_enable)
    countrotary = gpiozero.DigitalInputDevice(pin_countrotary, pull_up=True, bounce_time=bouncetime_rotary)
    hook = gpiozero.DigitalInputDevice(pin_hook, pull_up=True, bounce_time=bouncetime_hook)
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--ip", default=osc_ip, help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=osc_port, help="The port the OSC server is listening on")
    args = parser.parse_args()
    global client 
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
