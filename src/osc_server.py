#!/usr/bin/env python3
import argparse
import math
from pythonosc import dispatcher
from pythonosc import osc_server


class OSCServer:
    ip = None
    port = None

    def __init__(self, ip = "127.0.0.1", port = "5005"):
        self.ip = ip
        self.port = port
        self.run_server()

    def run_server(self):
        dispatcher_inst = dispatcher.Dispatcher()
        dispatcher_inst.map("/filter", print)
        dispatcher_inst.map("/volume", self.print_volume_handler, "Volume")
        dispatcher_inst.map("/logvolume", self.print_compute_handler, "Log volume", math.log)

        server = osc_server.ThreadingOSCUDPServer(
            (self.ip, self.port), dispatcher)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()

    @staticmethod
    def print_volume_handler(unused_addr, args, volume):
        print("[{0}] ~ {1}".format(args[0], volume))

    @staticmethod
    def print_compute_handler(unused_addr, args, volume):
        try:
            print("[{0}] ~ {1}".format(args[0], args[1](volume)))
        except ValueError:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    osc_server = OSCServer(args.ip, args.port)


