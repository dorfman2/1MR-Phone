"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import time
import configparser
from pythonosc import udp_client

config = configparser.ConfigParser()
config.read('config.ini')

osc_ip = config.get('osc', 'ip')
osc_port = int(config.get('osc', 'port'))

global client

x = 0
                 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=osc_ip, help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=osc_port, help="The port the OSC server is listening on")
    args = parser.parse_args()
    client = udp_client.SimpleUDPClient(args.ip, args.port)
    
if __name__ == "__main__":    
    for x in range(50):
        try:
            client.send_message("Playing Track %s" % 5, x)
        except:
             pass
        print("sent message %s.\n" % x)
        x = x + 1
        time.sleep(1)
