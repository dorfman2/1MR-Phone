1MR MP3 Rotary Telephone
-----
Description
-----
This module contains python 3 script to operate an interactive, rotary telephone. It plays back different audio files when different numbers are dialed. It features an OSC client to provide interactivity with audio & video elements on the same network. 

It can be used without untilizing OSC, but be sure to install the dependacy unless you want to comment out all the references
    
This phone was designed and built for a interactive performance called One Mile Radius Project(1MR for short).

-----
Installation
-----

Dependencies;

    * Git
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

        $ sudo apt-get update && apt-get upgrade -y
        
Install Python3, mpg123, and python3-pip

.. code-block:: bash

        $ sudo apt-get install python3 python3-pip mpg123 python3-gpiozero
        
Install 1MR-Phone using pip:

.. code-block:: bash

        $ pip install 1MR-Phone

Make /usr/bin/phone executable:

.. code-block:: bash

        $ sudo chmod +x /home/pi/1MR-Phone/phone.py


Copy your MP3 Files to /media, rename them to digits you want to be dialed "123.mp3."

I prefer to use FileZilla for this.

        
Append rc.local if you want this to run at boot.

.. code-block:: bash

        $ sudo sed -i -e '$i \/home/pi/1MR-Phone/./phone.py &\n' /etc/rc.local
       

 

Use
-----

Hardware
-----
List

* Rotary Telephone
* Raspberry Pi w/ Memory card
* 5v Power Supply
* Ethernet Cable

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
- Reciever = 24 (Hardware Pin 18)

5. Connect to ethernet
6. connect to Power

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
    
-----------------
Original Comments
-----------------
    
    > This Uses Open SoundControl for Python
    > Copyright (C) 2002 Daniel Holth, Clinton McChesney
    > 
    > This library is free software; you can redistribute it and/or modify it under
    > the terms of the GNU Lesser General Public License as published by the Free
    > Software Foundation; either version 2.1 of the License, or (at your option) any
    > later version.
    > 
    > This library is distributed in the hope that it will be useful, but WITHOUT ANY
    > WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
    > PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
    > details.
    
    > You should have received a copy of the GNU Lesser General Public License along
    > with this library; if not, write to the Free Software Foundation, Inc., 59
    > Temple Place, Suite 330, Boston, MA  02111-1307  USA
    
    > For questions regarding this module contact Daniel Holth <dholth@stetson.edu>
    > or visit http://www.stetson.edu/~ProctoLogic/
