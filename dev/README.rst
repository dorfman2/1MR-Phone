=====
Audio USB Notes
=====

Steps I've tried
-----

.. code-block:: bash
    
        $ sudo rpi-update #(Not needed but useful)
        $ arecord --device=hw:1,0 --format S16_LE --rate 44100 -V mono -c1 test.wav # To record
        

Notes from Adafruit
-----

At least with the CM-Headphone type adapter, you can also record audio.

:code: $ arecord --device=hw:1,0 --format S16_LE --rate 44100 -c1 test.wav

Will record signed 16-bit (S16_LE) audio at 44100 Hz (--rate 44100) mono (-c1) audio to test.wav. We've noted that any audio input will be echoed out the speakers as well
You can have a little VU meter show up if you add to the-V mono command line. Press control-C to quit

Once you're done recording you can play back with
:code: $ aplay --device=plughw:1,0 test.wav