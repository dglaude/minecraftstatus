#!/usr/bin/env python
"""Checks the status (availability, logged-in players) on a Minecraft server.
Display the count of user on a Blinkt! using ambiant color with all LED.
This is supposed to be used in a IKEA FADO lamp.

Fading indication to avoid annoying blinking:
Fade-in Fade-out of red mean the server is not reachable.
Fade-in Fade-out of green mean the server is up but noone is connected.
Fade-in Fade-out of green with a number of fade of blue that indicate the number of connected user.

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

from blinkt import set_pixel, show, set_brightness
from time import sleep

def FadeInOut(delay):
  for b in range(31):
    set_brightness(b/31.0)
    show()
    sleep(delay)
  for b in range(31):
    set_brightness((31-b)/31.0)
    show()
    sleep(delay)

def fade_count(n, r, g, b, fast=None):
    if fast is None:
        delay=0.0625
    else: 
        delay=0.015625
    for j in range (n):
        for i in range(8):
            set_pixel(i, r, g, b, 0)
        FadeInOut(delay)

logging.basicConfig(
    format='%(levelname)s %(asctime)s %(filename)s:%(lineno)s: %(message)s',
    level=logging.DEBUG)
#logging.getLogger().setLevel(logging.CRITICAL)

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
    n=server.num_players_online
    fade_count(n,0,0,255,1)   # Fast blue fade for number of player
    fade_count(1,0,255,0)     # Slow green fade to say the server is OK
  else:
    logging.info('unavailable')
    fade_count(1,255,0,0)     # Slow red fade to say the server is OK

