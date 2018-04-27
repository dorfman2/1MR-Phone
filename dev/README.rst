=====
Audio USB Notes
=====

Steps I've tried
-----

To set USB audio to ALSA default device, copy ''asound.conf'' to ''/etc/''


Useful commands

.. code-block:: bash
    
        $ sudo rpi-update #(Not needed but useful)
        $ arecord --device=hw:1,0 --format S16_LE --rate 44100 -V mono -c1 test.wav # To record
        $ amixer scontrols #list controls
        $ alsamixer -c 1 # Brings up digital faders for default 
        $ amixer set 'Auto Gain Control' on # turn on Auto Gain Control
        $ amixer set Speaker 100% # Max Volume
        

Notes from Adafruit
-----

At least with the CM-Headphone type adapter, you can also record audio.

    '$ arecord --device=hw:1,0 --format S16_LE --rate 44100 -c1 test.wav'

Will record signed 16-bit (S16_LE) audio at 44100 Hz (--rate 44100) mono (-c1) audio to test.wav. We've noted that any audio input will be echoed out the speakers as well
You can have a little VU meter show up if you add to the-V mono command line. Press control-C to quit

Once you're done recording you can play back with

    '$ aplay --device=plughw:1,0 test.wav'
    
    
Audio Device Information
-----

Audio USB adapter from Adafruit

- Simple mixer control 'Speaker',0
- Simple mixer control 'Mic',0
- Simple mixer control 'Auto Gain Control',0