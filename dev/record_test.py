#!/usr/bin/python3

import time
import subprocess

global current_time

if __name__ == "__main__":
    self = True
    print("Starting Recording for 10 Seconds")
    current_time = time.asctime( time.localtime(time.time()) )
    self.recorder = subprocess.Popen(["arecord -q --device=hw:1,0 --format S16_LE --rate 44100 -c1", current_time + ".wav"], shell=True)
    time.sleep(10)
    print("Recording Stopped, starting playback.")
    
    try:
        self.recorder.kill()
    except:
        pass
    
    self.player = subprocess.Popen(["mpg123", "-q", current_time + ".wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(10)
    exit(0)