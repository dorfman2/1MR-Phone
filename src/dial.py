#!/usr/bin/env python3
import subprocess
import os
from microphone import Microphone


class Dial:
    def __init__(self, track_limit):
        self.pulses = 0
        self.number = ""
        self.counting = True
        self.calling = False
        self.microphone = Microphone(track_limit)

    def startcalling(self):
        self.calling = True
        try:
            client.send_message("/Phone/" + phone_id + "/Pickup", 50)
        except:
            pass
        print("Pickup")
        self.player = subprocess.Popen(["aplay", "-q", "--device=plughw:1,0", "/home/pi/1MR-Phone/media/dialtone.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
                shutdown()
                return

            if self.number == "7867":  # If you dial "STOP" restarts
                restart()
                return

            if self.number == "732":  # start recording audio
                try:
                    self.player.kill()
                except:
                    pass

                self.microphone.recordStart()
                return

            elif os.path.isfile("/home/pi/1MR-Phone/media/" + self.number + ".wav"):
                print("start player with number = %s" % self.number)

                try:
                    self.player.kill()
                except:
                    pass

                try:
                    client.send_message("/Phone/" + phone_id + "/Track/" + self.number, self.number)
                except:
                    pass

                self.player = subprocess.Popen \
                    (["aplay", "-q", "--device=plughw:1,0", "/home/pi/1MR-Phone/media/" + self.number + ".wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
            self.player.kill()
            self.microphone.recordStop()
            client.send_message("/Phone/" + phone_id + "/Hangup", 51)
        except:
            pass
        print ("Hangup")
        self.pulses = 0
        self.number = ""