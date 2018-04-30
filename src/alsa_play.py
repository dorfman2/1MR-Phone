#!/usr/bin/env python3
import subprocess
import os

# Class to play sounds


class ALSAPlay:
    media_folder = None
    playback_hw_device = None
    player_subprocess = None

    def __init__(self, playback_hw_device, media_folder):
        if media_folder.endswith('/'):
            media_folder = media_folder[:-1]
        self.media_folder = media_folder

        self.playback_hw_device = playback_hw_device

    def get_media_path(self, media_file):
        path = "%s/%s" % (self.media_folder, media_file)
        return path

    # Searches for a arbitrary file
    def check_for_file(self, file_name):
        path = self.get_media_path(file_name)
        check = os.path.isfile(path)
        return check

    def play(self, file_name):
        if not self.check_for_file(file_name):
            print("Tried to play invalid file: %s" % file_name)
            return False

        path = self.get_media_path(file_name)
        command = [
            "aplay",
            "-q",
            "--device=%s" % self.playback_hw_device,
            path
        ]
        self.player_subprocess = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE)

    def stop(self):
        if self.player_subprocess is None:
            return False

        poll = self.player_subprocess.poll()
        if poll is None:
            self.player_subprocess.kill()
            return True

        return False



