#!/usr/bin/env python
"""Checks the status (availability, logged-in players) on a Minecraft server.
Display the count of user on a Blinkt! using one blue LED per user.
Blinking red mean server is down or cannot connect.

Example:
    $ %(prog)s host [port]
    available, 3 online: mf, dignity, viking

Based on:
    https://gist.github.com/barneygale/1209061
Protocol reference:
    http://wiki.vg/Server_List_Ping

By default the code log on the terminal the number of connected user.
This can be disabled by removing the hash in front of the folowing line:
#logging.getLogger().setLevel(logging.CRITICAL)
"""

import argparse
import logging

from mcstatus import McServer 

DEFAULT_PORT = 25565

from blinkt import set_pixel, show
from time import sleep

def blink():
    for i in range(5):
        set_pixel(7, 255, 0, 0)
        show()
        sleep(1)
        set_pixel(7, 0, 0, 0)
        show()
        sleep(1)

def show_n(n):
    for i in range(8):
        set_pixel(i, 0, 0, 0)
    show()
    sleep(1)
    for i in range(8):
        if n > i:
            set_pixel(i, 0, 0, 255)
        else:
            set_pixel(i, 0, 0, 0)
        show()
        sleep(1)
    sleep(1)

logging.basicConfig(
    format='%(levelname)s %(asctime)s %(filename)s:%(lineno)s: %(message)s',
    level=logging.DEBUG)
logging.getLogger().setLevel(logging.CRITICAL)

summary_line, _, main_doc = __doc__.partition('\n\n')
parser = argparse.ArgumentParser(
    description=summary_line,
    epilog=main_doc,
    formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument(
    '--port', type=int, default=DEFAULT_PORT,
    help='defaults to %d' % DEFAULT_PORT)
parser.add_argument('host')
args = parser.parse_args()

logging.info('querying %s:%d', args.host, args.port)

while True:
  server = McServer(args.host, port=args.port)
  server.Update()
  if server.available:
    logging.info(
        'available, %d online: %s',
        server.num_players_online,
        ', '.join(server.player_names_sample))
    show_n(server.num_players_online)
    sleep(5)
  else:
    logging.info('unavailable')
    blink()
