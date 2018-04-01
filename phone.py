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
import redis
import json

# Folder of this python script
DIR_PATH = os.path.dirname(os.path.realpath(__file__))



global start

start = True



# ===== Class Definitions =====
class Dial():
    client = None
    redis = None

    def __init__(self):
        self.pulses = 0
        self.number = ""
        self.counting = True
        self.calling = False
        self.client = None
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def ack_message(self):
        self.send_message("Sending null message", 1)

    def send_message(self, message, number):
        python_dict = {
            "message": message,
            "number": number
        }
        json_string = json.dumps(python_dict)

        # Push message onto the redis queue
        self.redis.lpush("osc_messages", json_string)

        # Truncates list to the newest five entries.
        self.redis.ltrim("osc_messages", 0, 5)

    def startcalling(self):
        self.calling = True
        self.send_message("cue/dialling", 1)
        self.player = subprocess.Popen(["mpg123", "-q", DIR_PATH + "/media/dialtone.mp3", ],
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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

            if self.number == "633":  # If you dial "OFF" turns off Phone
                self.send_message("Phone has entered Shutdown", 1)
                shutdown()
                return
            
            sound_file_path = DIR_PATH + "/media/" + self.number + ".mp3"
            print(sound_file_path)

            if self.number == "7867":  # If you dial "STOP" exits python script, comment out once debugging is complete
                self.send_message("Phone has closed program, please restart to enable", 1)
                close()
                return

            elif os.path.isfile(sound_file_path):
                print("start player with number = %s" % self.number)

                try:
                    self.player.kill()

                except:
                    pass

                self.send_message("cue/" + self.number + "/fire", self.number)
                self.player = subprocess.Popen(["mpg123", sound_file_path, "-q"],
                                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
        print("Hangup")
        self.send_message("cue/hangup", 1)
        self.pulses = 0
        self.number = ""
        try:
            self.player.kill()
        except:
            pass


# OSC Class - possibly pull out
class OSCClient:
    ip = None
    port = None
    client = None
    redis = None

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.connect()
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def connect(self):
        self.client = udp_client.SimpleUDPClient(self.ip, self.port)

    def process_queue(self):
        if self.redis.llen('osc_messages') < 1:
            return False
        json_text = self.redis.lpop('osc_messages')
        message_dict = json.loads(json_text)
        result = self.send_message(message_dict['string'], message_dict['number'])
        if result is False:
            # Turn message_dict back into JSON and push back into redis
            # so we can try to send the OSC message again on the next
            # iteration.
            json_text = json.dumps(message_dict)
            self.redis.rpush("osc_messages", json_text)

    def send_message(self, string, number):
        try:
            self.send_message(string, number)
            return True
        except:
            print("Couldn't send!!!")
            print("Reconnecting!")
            self.connect()
            return False


def gpio_loop(config):
    dial = Dial()
    # Your phone GPIO pins, using BCIM numbers
    pin_rotary_enable = int(config.get('pin', 'rotaryenable'))  # Clockwise Rotary Circuit
    pin_count_rotary = int(config.get('pin', 'countrotary'))  # Counter-clockwise Rotary Circuit
    pin_hook = int(config.get('pin', 'hook'))  # Hook or hangup Switch

    bounce_time_enable = float(config.get('bouncetime', 'enable'))
    bounce_time_rotary = float(config.get('bouncetime', 'rotary'))
    bounce_time_hook = float(config.get('bouncetime', 'hook'))

    # Define Pins
    rotary_enable = gpiozero.DigitalInputDevice(pin_rotary_enable, pull_up=True, bounce_time=bounce_time_enable)
    count_rotary = gpiozero.DigitalInputDevice(pin_count_rotary, pull_up=True, bounce_time=bounce_time_rotary)
    hook = gpiozero.DigitalInputDevice(pin_hook, pull_up=True, bounce_time=bounce_time_hook)

    count_rotary.when_deactivated = dial.addpulse
    count_rotary.when_activated = dial.addpulse

    rotary_enable.when_activated = dial.startcounting
    rotary_enable.when_deactivated = dial.stopcounting

    hook.when_activated = dial.stopcalling
    hook.when_deactivated = dial.startcalling
    while True:
        time.sleep(1)


def osc_loop(osc_ip, osc_port):
    osc_object = OSCClient(osc_ip, osc_port)
    while True:
        osc_object.process_queue()
        time.sleep(0.2)


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    osc_ip = config.get('osc', 'ip')
    osc_port = int(config.get('osc', 'port'))

    parser = argparse.ArgumentParser()

    parser.add_argument("--ip", default=osc_ip, help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=osc_port, help="The port the OSC server is listening on")
    args = parser.parse_args()

    pid = os.fork()
    if pid == 0:
        gpio_loop(config)
    else:
        osc_loop(args.ip, args.port)


def shutdown():
    subprocess.Popen(["sudo shutdown -h now"], shell=True)


def close():
    exit(0)


if __name__ == "__main__":
    main()
