# Make phone.py executable
sudo chmod x /home/pi/1MR-Phone/phone.py

# This is to append rc.local to start phone on boot
sed -i -e '$i \/home/pi/1MR-Phone/./phone &\n' rc.local
