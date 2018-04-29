#!/usr/bin/python3
# 1MR-Phone Version 2.4
# 24 March, 2018
# Written by Jeffrey Dorfman, with help from Aaron Saderholm, based on code from Raaff (https://github.com/Raaff)
# 1 Mile Radius Telephone is an interactive rotary telephone created for the 1 Mile Radius Project.

import subprocess
import time
import configparser


def shutdown():
    subprocess.Popen(["mpg123", "-q", "/home/pi/1MR-Phone/media/shutdown.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)
    subprocess.Popen(["sudo shutdown -h now"], shell=True)
    
    
def restart():
    subprocess.Popen(["mpg123", "-q", "/home/pi/1MR-Phone/media/restart.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)
    subprocess.Popen(["sudo reboot"], shell=True)


def main():
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
    pin_rotaryenable = int(config.get('pin', 'rotaryenable'))  # Clockwise Rotary Circuit
    pin_countrotary = int(config.get('pin', 'countrotary'))  # Counter-clockwise Rotary Circuit
    pin_hook = int(config.get('pin', 'hook'))  # Hook or hangup Switch

    # Bouncetimes
    bouncetime_enable = float(config.get('bouncetime', 'enable'))
    bouncetime_rotary = float(config.get('bouncetime', 'rotary'))
    bouncetime_hook = float(config.get('bouncetime', 'hook'))

    subprocess.Popen(["amixer -q set Speaker 100%"], shell=True)  # Sets the volume to 0db (maximum)
    subprocess.Popen(["amixer -q set Mic 25%"], shell=True)
    # subprocess.Popen(["amixer -q set 'Auto Gain Control' on"], shell=True)



