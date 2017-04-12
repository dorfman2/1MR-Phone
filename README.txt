DESCRIPTION
    This module contains python script to operate an interactive, rotary telephone. It plays back different audio files when different numbers are dialed.
    
    ================
    1 Mile Radius Rotary Telephone
    ================


    ----------
    HARDWARE
    ----------

    Open up your phone. Remove the circuit board and bells. Be sure to keep the wires leading to the rotary, as well as the handset and handset switch.
    
    ----------
    Changelog:
    ----------
    v1.0  - 14 Mar. 2017
            Modified script created by https://gist.github.com/simonjenny/8d6c29db8b8a995a4d89
            Commited V1.0

    v1.1.2  - 29 Mar. 2017
            Added OSC capabilites for external interactive elements using pyOSC and Dial Tone.
    
    
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
    

INSTALLING

REQUIRES INSTALLATION OF;

    Git
    https://github.com/IanShelanskey/pyosc
    python3 
    python3-rpi.gpio 
    mpg123
    
Boot up the RaspberryPi and login. First update your Repositories:

        $ sudo apt-get update && apt-get upgrade -y
        
Install Python3, Python GPIO, mpg123, and python3-pip

        $ sudo apt-get install python3 python3-rpi.gpio mpg123 python3-pip
        
Install python-osc (for OSC transmission. This is optional, but you'll need to comment out the OSC lines in the code if you skip this)

        $ sudo pip3 install python-osc
        
Create a file in /usr/bin

        $ sudo nano /usr/bin/phone
        
Copy phone.py code to /usr/bin/phone:

        $ sudo

Make /usr/bin/phone executable:

        $ sudo chmod a+x /usr/bin/phone


Copy your MP3 Files to /media, rename them to 0.mp3, 1.mp3 ... 9.mp3

Create playlists for each number in /media, call them 0.m3u, 1.m3u, ... 9.m3u

Test your phone first :

        /usr/bin/./phone
        
        
Update /etc/rc.local

        sudo nano /etc/rc.local
        
        
and insert this script before exit 0;

        /usr/bin/./phone &



    

DOCUMENTATION

Following are the steps to be followed to install python3's setuptools and SPARQLWrapper

sudo apt-get install python3-setuptools
sudo easy_install3 pip
pip -V This should show the pip corresponding to your python3 installation.
    
TESTING

Commands I found useful in debugging

    $ sudo killall -9 mpg123
    $
