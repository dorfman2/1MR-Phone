#!/usr/bin/env python3
import subprocess
import time
import os
import shlex


class Microphone:
    rec_subprocess = None
    track_count = 0
    track_limit = 0

    def get_track_name(self):
        file_name = "%s.wav" % self.track_count
        return "%s/%s" % (self.recording_path, file_name)

    def __init__(self, recording_path, track_count=0, track_limit=2):
        self.base_epoch = int(time.time())
        self.track_count = track_count
        self.track_limit = track_limit
        self.recording_path = recording_path

    def record_start(self):
        self.track_count += 1
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

        if self.track_count >= self.track_limit:
            self.track_count = 0
        return file_name

    def record_stop(self):
        self.rec_subprocess.kill()
