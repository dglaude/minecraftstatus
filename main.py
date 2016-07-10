#!/usr/bin/env python
"""Checks the status (availability, logged-in players) on a Minecraft server.

Example:
    $ %(prog)s host [port]
    available, 3 online: mf, dignity, viking

Based on:
    https://gist.github.com/barneygale/1209061
Protocol reference:
    http://wiki.vg/Server_List_Ping
"""

import argparse
import logging

from mcstatus import McServer 

DEFAULT_PORT = 25565
TIMEOUT_SEC = 5.0

if __name__ == '__main__':
  logging.basicConfig(
      format='%(levelname)s %(asctime)s %(filename)s:%(lineno)s: %(message)s',
      level=logging.DEBUG)

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

  server = McServer(args.host, port=args.port)
  server.Update()
  if server.available:
    logging.info(
        'available, %d online: %s',
        server.num_players_online,
        ', '.join(server.player_names_sample))
  else:
    logging.info('unavailable')
