#!/usr/bin/env python3
import math
from pythonosc import udp_client as osc_udp_client


class Dial:

    def __init__(self, audio_player, microphone, phone_id, osc_ip=False, osc_port=False):
        self.pulses = 0
        self.number = ""
        self.counting = True
        self.calling = False
        self.microphone = microphone
        self.phone_id = phone_id
        self.player = audio_player

        if osc_ip:
            self.osc_client = osc_udp_client.SimpleUDPClient(osc_ip, osc_port)
        else:
            self.osc_client = None

    def osc_message(self, message, value):
        message = "/Phone/%s/%s" % (self.phone_id, message)
        if self.osc_client is None:
            print("OSC Transmission: %s (Value %s) (No OSC Connection)" % (message, value))
        else:
            print("OSC Transmission: %s (Value %s)" % (message, value))
            self.osc_client.send_message(message, value)

    def start_calling(self):
        self.calling = True
        self.osc_message("Pickup", 50)
        print("Pickup")
        self.player.play("dialtone.wav")

    def stop_calling(self):
        self.calling = False
        self.reset()

    def start_counting(self):
        self.counting = self.calling

    def stop_counting(self):
        if self.calling:
            if self.pulses > 0:
                if math.floor(self.pulses / 2) == 10:
                    self.number += "0"
                else:
                    self.number += str(math.floor(self.pulses / 2))

            self.pulses = 0

            if self.number == "633":  # If you dial "OFF" turns off Phone
                print("Would shutdown but not implemented.")
                return

            if self.number == "7867":  # If you dial "STOP" restarts
                print("Would restart but not implemented.")
                return

            if self.number == "732":  # start recording audio
                self.player.stop()
                self.microphone.record_start()
                return

            if self.player.check_for_file("%s.wav" % self.number):
                print("start player with number = %s" % self.number)
                self.player.stop()
                self.osc_client.send_message("Track/%s" % self.number, self.number)

                media_file = "%s.wav" % self.number
                self.player.play(media_file)
                return

        print("Stop counting. Got number %s.\n" % self.number)
        self.counting = False

    def add_pulse(self):
        print("add-pulse")
        if self.counting:
            print("real add-pulse")
            self.pulses += 1

    def get_number(self):
        return self.number

    def reset(self):
        self.player.stop()
        self.microphone.record_stop()
        self.osc_message("Hangup", 51)
        print("Hangup")
        self.pulses = 0
        self.number = None
