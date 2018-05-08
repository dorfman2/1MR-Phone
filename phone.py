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
import pickle
from pythonosc import udp_client


# ===== Global Variables =====
global client
global start
start = True


# ===== Config.ini =====
config = configparser.ConfigParser()
config.read('config.ini')

    
# ===== Variables (called from config.ini)=====


# Phone Settings
track_limit = int(config.get('phone', 'track_limit'))
track_count = int(config.get('phone', 'track_start'))
#speaker_volume = str(config.get('phone', 'speaker_volume'))
#mic_volume = str(config.get('phone', 'mic_volume')) 


# OSC Settings
phone_id = config.get('osc', 'id')
osc_enable = config.get('osc', 'osc')
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


subprocess.Popen(["amixer -q set Speaker 80%"], shell=True) # Sets the volume to 0db (maximum)
subprocess.Popen(["amixer -q set Mic 20%"], shell=True)
#subprocess.Popen(["amixer -q set 'Auto Gain Control' on"], shell=True)



# ===== Class Definitions =====

class Microphone():
    rec_subprocess = None
    

    def get_track_name(self):
        dir_name = "/home/pi/1MR-Phone/media"
        file_name = "%s.wav" % (self.track_count)
        return "%s/%s" % (dir_name, file_name)
    
    def __init__(self, track_count=0, track_limit=2):
        self.base_epoch = int(time.time())
        self.track_count = track_count
        self.track_limit = track_limit
        
        try:
            with open ('persistant_track_count.pickle', 'rb') as handle:     
                self.recorded_track_count = pickle.load(handle)
        except FileNotFoundError:
            self.recorded_track_count = track_count
            with open('persistant_track_count.pickle', 'wb') as handle:
                pickle.dump(self.recorded_track_count, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        if self.recorded_track_count >= track_count:
            self.track_count = self.recorded_track_count
                
            
    def recordStart(self):
        self.track_count += 1
        self.recorded_track_count = self.track_count
        with open('persistant_track_count.pickle', 'wb') as handle:
            pickle.dump(self.recorded_track_count, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("Recording pickle to %s" % self.recorded_track_count)
     
        os.system("pkill -f /usr/bin/arecord")
        time.sleep(0.1)
        file_name = self.get_track_name()
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
    
    
    def trackCountReset(self):
        self.track_count = int(config.get('phone', 'track_start'))
        self.recorded_track_count = self.track_count
        with open('persistant_track_count.pickle', 'wb') as handle:
            pickle.dump(self.recorded_track_count, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(" Track Count has been reset to %s.\n Update config file to change this default.\n" % self.recorded_track_count)


class Dial():
    def __init__(self, track_count, track_limit):
        self.pulses = 0
        self.number = ""
        self.counting = True
        self.calling = False
        self.microphone = Microphone(track_count, track_limit)


    def startcalling(self):
        self.calling = True
        try:
            client.send_message("/Phone/" + phone_id + "/Pickup", 50)
        except:
             pass
        print(" Pickup")
        self.player = subprocess.Popen(["aplay", "-q", "--device=plughw:1,0", "/home/pi/1MR-Phone/media/dialtone.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def stopcalling(self):
        self.calling = False
        self.reset()

    def startcounting(self):
        self.counting = self.calling

    def stopcounting(self):
        try:
            self.player.kill()
        except:
            pass
        if self.calling:
            if self.pulses > 0:
                if math.floor(self.pulses / 2) == 10:
                    self.number += "0"
                else:
                    self.number += str(math.floor(self.pulses / 2))

            self.pulses = 0
            
            if self.number == "633": #If you dial "OFF" turns off Phone
                try:
                    self.player.kill()
                except:
                    pass
                print(" Phone is shutting down")
                self.shutdown()
                return
            
            if self.number == "737": #If you dial "RES" restarts
                try:
                    self.player.kill()
                except:
                    pass
                print(" Phone is restarting")
                self.restart()
                return
            
            if self.number == "0": #start recording audio
                try:
                    self.player.kill()
                except:
                    pass
                self.player = subprocess.Popen(["aplay", "-q", "--device=plughw:1,0", "/home/pi/1MR-Phone/media/leave_message.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                time.sleep(4) # should be 4 seconds
                self.microphone.recordStart()
                return
            
            if self.number == "826": #dial "TCO" Reset Track count to value specified in config.ini
                try:
                    self.player.kill()
                except:
                    pass
                self.player = subprocess.Popen(["aplay", "-q", "--device=plughw:1,0", "/home/pi/1MR-Phone/media/track_count_reset.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.microphone.trackCountReset()
                return
            
            elif os.path.isfile("/home/pi/1MR-Phone/media/" + self.number + ".wav"):
                print(" Start player with number = %s\n" % self.number)
                
                try:
                    self.player.kill()
                except:
                    pass
                
                try:
                    client.send_message("/Phone/" + phone_id + "/Track/" + self.number, self.number)
                except:
                    pass

                self.player = subprocess.Popen(["aplay", "-q", "--device=plughw:1,0", "/home/pi/1MR-Phone/media/" + self.number + ".wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(" Stop counting. Got number %s.\n" % self.number)
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
           self.player.kill()
           self.microphone.recordStop()
           client.send_message("/Phone/" + phone_id + "/Hangup", 51)
        except:
             pass
        print (" Hangup")
        self.pulses = 0
        self.number = ""

    def shutdown(self):
        subprocess.Popen(["aplay", "-q", "--device=plughw:1,0", "/home/pi/1MR-Phone/media/shutdown.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        subprocess.Popen(["sudo shutdown -h now"], shell=True)
        
        
    def restart(self):
        subprocess.Popen(["aplay", "-q", "--device=plughw:1,0", "/home/pi/1MR-Phone/media/restart.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        subprocess.Popen(["sudo reboot"], shell=True)
            
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

    dial = Dial(track_count=track_count, track_limit=track_limit)
    countrotary.when_deactivated = dial.addpulse
    countrotary.when_activated = dial.addpulse
    rotaryenable.when_activated = dial.startcounting
    rotaryenable.when_deactivated = dial.stopcounting
    hook.when_activated = dial.stopcalling
    hook.when_deactivated = dial.startcalling
    while True:
        time.sleep(0.5)