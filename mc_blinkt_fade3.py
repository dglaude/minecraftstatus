#!/usr/bin/env python
"""Checks the status (availability, logged-in players) on a Minecraft server.

Display the count of user on a Blinkt! using ambiant color with all LED.

This is exactly like previous version with fade set by turning on and off from 0 to 8 LEDs. But the brightness is set based on the hour of the day, assuming during night, less brightness can be used. Since the Blinkt! is supposed to be inside a FADO lamp from IKEA, individual LEDs are not visible.

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
import datetime

from mcstatus import McServer 

DEFAULT_PORT = 25565

from blinkt import set_pixel, show, set_brightness
from time import sleep

hour2bright= [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]

def fade_count(n, r, g, b, delay, bright=1.0):

  for j in range (n):
    for i in range(8):
      set_pixel(i, r, g, b, bright)
      show()
      sleep(delay)
    for i in range(8):
      set_pixel(i, 0, 0, 0, bright)
      show()
      sleep(delay)

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
  bright=hour2bright[datetime.datetime.now().hour]
  for x in range(60):
    server = McServer(args.host, port=args.port)
    server.Update()
    if server.available:
      logging.info(
        'available, %d online: %s',
        server.num_players_online,
        ', '.join(server.player_names_sample))
      n=server.num_players_online
      fade_count(n,0,0,255,1.0/16,bright)   # Fast blue fade for number of player
      fade_count(1,0,255,0,1.0/8,bright)     # Slow green fade to say the server is OK
    else:
      logging.info('unavailable',bright)
      fade_count(1,255,0,0,1.0/8)     # Slow red fade to say the server is OK

