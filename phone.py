#!/usr/bin/python3

# 1MR-Phone Version 2.4 
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
import os
import time
import configparser
import argparse
import shlex
from pythonosc import udp_client


# ===== Global Variables =====
global client
global start
start = True


# ===== Config.ini =====
config = configparser.ConfigParser()
config.read('config.ini')

    
# ===== Variables (called from config.ini)=====

# Your phone ID, if using multiple phones
phone_id = config.get('phone', 'id')
osc_enable = config.get('phone', 'osc')
track_limit = int(config.get('phone', 'track_limit'))


osc_ip = config.get('osc', 'ip')
osc_port = int(config.get('osc', 'port'))

# Your phone GPIO pins, using BCIM numbers
pin_rotaryenable = int(config.get('pin', 'rotaryenable')) #Clockwise Rotary Circuit
pin_countrotary = int(config.get('pin', 'countrotary'))   #Counter-clockwise Rotary Circuit
pin_hook = int(config.get('pin', 'hook'))                     #Hook or hangup Switch
    

# Bouncetimes
bouncetime_enable = float(config.get('bouncetime', 'enable'))
bouncetime_rotary = float(config.get('bouncetime', 'rotary'))
bouncetime_hook = float(config.get('bouncetime', 'hook'))


subprocess.Popen(["amixer -q set Speaker 100%"], shell=True) # Sets the volume to 0db (maximum)
subprocess.Popen(["amixer -q set Mic 25%"], shell=True)
#subprocess.Popen(["amixer -q set 'Auto Gain Control' on"], shell=True)


# ===== Class Definitions =====


class Microphone():
    
    rec_subprocess = None
    track_count = 0
    track_limit = 0
    
    
    def __init__(self, track_count=0, track_limit=99):
        self.track_count = track_count
        self.track_limit = track_limit
        
        
    def get_track_name(self):
        dir_name = "/home/pi/1MR-Phone/media"
        file_name = "%s.wav" % (self.track_count)
        return "%s/%s" % (dir_name, file_name)
    
                
    def recordStart(self):
        self.track_count += 1
        os.system("pkill -f /usr/bin/arecord")
        time.sleep(0.1)
        file_name = self.get_track_name()
        self.player.play("leaveMessage")
        time.sleep(2)
        print("Recording to %s" % file_name)
        command = "/usr/bin/arecord --device=hw:1,0 --format=S16_LE --rate=44100 -c1 %s" % file_name
        args = shlex.split(command)

        self.rec_subprocess = subprocess.Popen(
                args,
                shell=False,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT)

        if (self.track_count >= self.track_limit):
            self.track_count = 0
        return file_name


    def recordStop(self):
        self.rec_subprocess.kill()
        


class Dial():

    
    def __init__(self, track_limit, track_name):
        self.pulses = 0
        self.number = ""
        self.counting = True
        self.calling = False
        self.track_name = track_name
        self.microphone = Microphone(0, track_limit)
        self.player = Player(track_name)


    def startcalling(self):
        self.calling = True
        try:
            client.send_message("/Phone/" + phone_id + "/Pickup", 50)
        except:
             pass
        print("Pickup")
        self.player.play("dialtone")


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
                self.shutdown()
                return
            
            if self.number == "738": #If you dial "RES" restarts
                self.restart()
                return
            
            if self.number == "732": #start recording audio
                try:
                    self.player.kill()
                except:
                    pass
                
                self.microphone.recordStart()
                return
            
            elif os.path.isfile("/home/pi/1MR-Phone/media/" + self.number + ".wav"):
                print("start player with number = %s" % self.number)
                
                try:
                    self.player.stop()
                except:
                    pass
                
                try:
                    client.send_message("/Phone/" + phone_id + "/Track/" + self.number, self.number)
                except:
                    pass

                self.player.play(self.number)
        
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
        try:
           self.player.stop()
           self.microphone.recordStop()
           client.send_message("/Phone/" + phone_id + "/Hangup", 51)
        except:
             pass
        print ("Hangup")
        self.pulses = 0
        self.number = ""


    def shutdown(self):
        self.reset()
        print("Phone entering shutdown in 3 seconds")
        self.player.play("shutdown")
        time.sleep(3)
        subprocess.Popen(["sudo shutdown -h now"], shell=True)
        
        
    def restart(self):
        self.reset()
        print("Phone rebooting in 3 seconds")
        self.player.play("restart")
        time.sleep(3)
        subprocess.Popen(["sudo reboot"], shell=True)


class Player():
    
    track_name = 0
    
    def __init__(self, track_name=0):
        self.track_name = track_name
    
    def play(self):
        self.player = subprocess.Popen(["aplay", "-q", "--device=plughw:1,0", "/home/pi/1MR-Phone/media/" + self.track_name + ".wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    def stop(self):
        try:
             self.player.play.kill()
        except:
            pass
                
    
        
# ===== Main Script =====

if __name__ == "__main__":

    if (osc_enable == "yes"):
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument("--ip", default=osc_ip, help="The ip of the OSC server")
            parser.add_argument("--port", type=int, default=osc_port, help="The port the OSC server is listening on")
            args = parser.parse_args()
            client = udp_client.SimpleUDPClient(args.ip, args.port)
        except:
            pass
    
    # Startup scripts
    if (start == 1):
        start = 0
        
        print("Phone On")
        try:
            client.send_message("/Phone/" + phone_id + "/ON", phone_id)
        except:
            pass
        
    rotaryenable = gpiozero.DigitalInputDevice(pin_rotaryenable, pull_up=True, bounce_time=bouncetime_enable)
    countrotary = gpiozero.DigitalInputDevice(pin_countrotary, pull_up=True, bounce_time=bouncetime_rotary)
    hook = gpiozero.DigitalInputDevice(pin_hook, pull_up=True, bounce_time=bouncetime_hook)

    dial = Dial(track_limit=track_limit, track_name=track_name)
    countrotary.when_deactivated = dial.addpulse
    countrotary.when_activated = dial.addpulse
    rotaryenable.when_activated = dial.startcounting
    rotaryenable.when_deactivated = dial.stopcounting
    hook.when_activated = dial.stopcalling
    hook.when_deactivated = dial.startcalling
    while True:
        time.sleep(0.5)