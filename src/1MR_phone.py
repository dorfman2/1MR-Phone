#!/usr/bin/python3
# 1MR-Phone Version 2.4
# 24 March, 2018
# Written by Jeffrey Dorfman, with help from Aaron Saderholm, based on code from Raaff (https://github.com/Raaff)
# 1 Mile Radius Telephone is an interactive rotary telephone created for the 1 Mile Radius Project.

import subprocess
import time
import configparser
import gpiozero
import argparse
from dial import Dial
from microphone import Microphone
from alsa_play import ALSAPlay


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    phone_id = config.get('phone', 'id')

    track_limit = int(config.get('phone', 'track_limit'))

    media_path = config.get('config', 'media_path')
    recording_path = config.get('config', 'recording_path')
    playback_hw_device = config.get('config', 'playback_hw_device')

    osc_enable = config.get('phone', 'osc')
    if osc_enable:
        osc_ip = config.get('osc', 'ip')
        osc_port = int(config.get('osc', 'port'))
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default=osc_ip, help="The ip of the OSC server")
        parser.add_argument("--port", type=int, default=osc_port, help="The port the OSC server is listening on")
        args = parser.parse_args()
        osc_ip = args.osc_ip
        osc_port = args.osc_port
    else:
        osc_ip = None
        osc_port = None

    # Setting up Audio
    subprocess.Popen(["amixer -q set Speaker 100%"], shell=True)  # Sets the volume to 0db (maximum)
    subprocess.Popen(["amixer -q set Mic 25%"], shell=True)
    # subprocess.Popen(["amixer -q set 'Auto Gain Control' on"], shell=True)

    audio_player = ALSAPlay(playback_hw_device, media_path)
    microphone = Microphone(recording_path=recording_path, track_limit=track_limit)

    dial = Dial(audio_player=audio_player, microphone=microphone, phone_id=phone_id, osc_ip=osc_ip, osc_port=osc_port)
    dial.osc_message("ON", phone_id)

    # Phone GPIO pins, using BCIM numbers
    pin_rotary_enable = int(config.get('pin', 'rotaryenable'))  # Clockwise Rotary Circuit
    pin_count_rotary = int(config.get('pin', 'countrotary'))  # Counter-clockwise Rotary Circuit
    pin_hook = int(config.get('pin', 'hook'))  # Hook or hangup Switch

    # Bounce times
    bounce_time_enable = float(config.get('bouncetime', 'enable'))
    bounce_time_rotary = float(config.get('bouncetime', 'rotary'))
    bounce_time_hook = float(config.get('bouncetime', 'hook'))

    rotary_enable = gpiozero.DigitalInputDevice(pin_rotary_enable, pull_up=True, bounce_time=bounce_time_enable)
    rotary_enable.when_activated = dial.start_counting
    rotary_enable.when_deactivated = dial.stop_counting

    count_rotary = gpiozero.DigitalInputDevice(pin_count_rotary, pull_up=True, bounce_time=bounce_time_rotary)
    count_rotary.when_deactivated = dial.add_pulse
    count_rotary.when_activated = dial.add_pulse

    hook = gpiozero.DigitalInputDevice(pin_hook, pull_up=True, bounce_time=bounce_time_hook)
    hook.when_activated = dial.stop_calling
    hook.when_deactivated = dial.start_calling

    print("Phone Ready")

    while True:
        time.sleep(0.5)


if __name__ == "__main__":
    main()