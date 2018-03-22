MP3 Rotary Telephone
-----
Description
-----
This module contains python 3 script to operate an interactive, rotary telephone. It plays back different audio files when different numbers are dialed. It features an OSC client to provide interactivity with audio & video elements on the same network. 

It can be used without untilizing OSC, but be sure to install the dependacy unless you want to comment out all the references
    
This phone was designed and built for a interactive performance called <strong>One Mile Radius Project</strong>.

-----
Installation
-----

Dependencies;

    Git
    gpiozero
    [python-osc](https://github.com/attwad/python-osc)
    python3
    python3-pip
    mpg123
    
To Install Dependencies 

Boot up the RaspberryPi and login. First update your Repositories:

        $ sudo apt-get update && apt-get upgrade -y
        
Install Python3, mpg123, and python3-pip

        $ sudo apt-get install python3 python3-pip mpg123 python3-gpiozero
        
Install 1MR-Phone using pip:

        $ pip install 1MR-Phone

Make /usr/bin/phone executable:

        $ sudo chmod a+x /usr/bin/phone


Copy your MP3 Files to /media, rename them to digits you want to be dialed "123.mp3."

        
Update /etc/rc.local

        $ sudo nano /etc/rc.local
       
and insert this script before exit 0;

        $ /home/pi/./phone &

  

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
3. Use a meter or some low voltage method to identify the wires connected to the;
..1. Dial Circuit - this is active when dialing
..2. Rotary Circuit - This is active when you release. Count the amount of clicks and it returns the number dialed.
..3. Reciever or Hook Circuit - The contact that reacts to if the phone is "hung up."
4. Connect these three circuits to ground, and three different GPIO pins. Not all GPIO pins are created equal, and this varies based on your Raspberry Pi model. I used for my Raspberry pi 2(With BCIM numbers);
..1. Dial = 18 (Hardware Pin 12)
..2. Ground (Hardware Pin 14)
..3. Rotary = 23 (Hardware Pin 16)
..4. Reciever = 24 (Hardware Pin 18)
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
