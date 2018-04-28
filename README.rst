=====
1MR-Phone
=====

An MP3 rotary telephone

-----
Description
-----
This module contains python 3 script to operate an interactive, rotary telephone. It plays back different audio files when different numbers are dialed. It features an OSC client to provide interactivity with audio & video elements on the same network. 

It can be used without using OSC.
    
This phone was designed and built for a interactive performance called One Mile Radius Project(1MR for short).

Version 1.1.2 was used for a performance in April 2017 with 3 phones
    
Version 2.3 was used for a performance in April 2018 with 5 phones


-----
Installation
-----

This was designed and built on Raspian Stretch Lite

Dependencies;

    * git
    * gpiozero
    * python-osc
    * python3
    * python3-pip
    * mpg123
  
      
-----
To Install Dependencies & 1MR-Phone
-----
Boot up the RaspberryPi and login. First update your Repositories:

.. code-block:: bash

        $ sudo apt-get update && sudo apt-get upgrade -y
        
Install Python3, mpg123, git, and python3-pip

.. code-block:: bash

        $ sudo apt-get install git python3 python3-pip mpg123 python3-gpiozero
        
Install python-osc

.. code-block:: bash

        $ sudo pip3 install python-osc
        
Navigate to your root directory (/home/pi) and install 1MR-Phone using pip:

.. code-block:: bash

        $ cd
        $ git clone https://github.com/dorfman2/1MR-Phone.git

        
Move sp.service to systemd if you want this to run at boot. Navigate to the folder first.

.. code-block:: bash

        $ cd /home/pi/1MR-Phone
        $ sudo cp sp.service /etc/systemd/system/sp.service
        $ sudo systemctl enable sp.service
        $ sudo systemctl daemon-reload
        
If you're using a USB sound card, copy the asound.conf file. You may have to edit it depending on your setup.
        
    .. code-block:: bash

        $ cd /home/pi/1MR-Phone
        $ sudo cp /dev/asound.conf /etc/asound.conf
    

       

 
Use
-----

* Copy your MP3 Files to /media, rename them to digits you want to be dialed "123.mp3."
** I prefer to use FileZilla for this. https://filezilla-project.org

* To make changes to ip/port address, phone ID, and bouncetimes, use "config.ini."

* For troubleshooting, you can start and stop the service by using these commands.

.. code-block:: bash
        
        $ sudo systemctl stop sp.service
        $ sudo systemctl start sp.service
        
* To disable the service entirely (you can renable it later)

.. code-block:: bash

        $ sudo systemctl disable sp.service
        $ sudo systemctl daemon-reload
        
        
Hardware
-----

* Rotary Telephone
* Raspberry Pi w/ Memory card
* 5v Power Supply
* Ethernet Cable
* 1/8" Male TRS connector
* (OPTIONAL) USB Sound Card


Build
-----
1. Open up your rotary telephone. 
2. Remove the circuit board and bells. Be sure to keep the wires leading to the rotary, as well as the handset and handset switch.
3. Use a meter or some low voltage method to identify the wires connected.

- Dial Circuit - this is active when dialing
- Rotary Circuit - This is active when you release. Count the amount of clicks and it returns the number dialed.
- Reciever or Hook Circuit - The contact that reacts to if the phone is "hung up."

4. Connect these three circuits to ground, and three different GPIO pins. Not all GPIO pins are created equal, and this varies based on your Raspberry Pi model. I used for my Raspberry pi 2(With BCIM numbers)

- Dial = 18 (Hardware Pin 12)
- Ground (Hardware Pin 14)
- Rotary = 23 (Hardware Pin 16)
- Reciever Switch = 24 (Hardware Pin 18)

5. Wire the two wires to the speaker in the Handset to 1/8" connector. You can use a USB audio card (OPTIONAL). I used Audio USB adapter from Adafruit.

- Speaker Negative to Sleeve
- Speaker Positive to Tip and Ring

5. Connect to ethernet
6. Connect to Power


----------
Changelog
----------
v1.0  - 14 Mar. 2017
    - Modified script created by https://gist.github.com/simonjenny/8d6c29db8b8a995a4d89
    - Commited V1.0

v1.1.2  - 29 Mar. 2017
    - Added OSC capabilites for external interactive elements using Python-osc and Dial Tone.
            
v2.0 - 21 Mar. 2018
    - Forked https://github.com/Raaff/rotarypi.git
        This added stability, shudown, and multi-digit dialling
        Utilizes new gpioZero library
    - Updated .md with a more accurate tutorial
    - removed TTS functions (since this will not be online)
    
V2.3 - April 2018
    - Added stability, cleaning, and Network error checks
    
