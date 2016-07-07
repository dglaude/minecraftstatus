# Number of user on a Minecraft server Indicator with Pimoroni's Blinkt

This is a merge from two independants project found on github:
- [bennuttall/people-in-space-indicator-blinkt](https://github.com/bennuttall/people-in-space-indicator-blinkt) People in Space Indicator with Pimoroni's Blinkt
- [markfickett/minecraftstatus](https://github.com/markfickett/minecraftstatus)
Check the status of a Minecraft server, including list of online players.

## Hardware

- Raspberry PiZero (v1.2)
- [Pimoroni Blinkt](https://shop.pimoroni.com/products/blinkt)
- USB cable
- MicroSD card
- Mac mini running the minecraft server

## Software

- [Pimoroni Blinkt Python library](https://github.com/pimoroni/blinkt)

## Usage

Run `mcstatus+blinkt.py server_name_or_ip` on a Pi terminal with connectivity to the minecraft server 

## Features

Every minute, it connect to a Minecraft server, query the number of connected user and it lights up an LED per user connected, in sequence.

If the Minecraft server is unavailable, the end LED blinks red.

## Notes

Very special setup (totally out of the scope of this project) for this Raspberry PiZero.
The PiZero get both network and power from the host (MAC mini) from a single USB cable. The setup was made based on this: [Setting up Pi Zero OTG - The quick way (No USB keyboard, mouse, HDMI monitor needed)](http://blog.gbaman.info/?p=791)
Additionnaly, the MAC mini is sharing it's internet connectivity for update and communication with remote Minecraft server.

## Learning resource

This project is based on a Raspberry Pi learning resource wrote by Ben Nuttall that just uses simple LEDs using [GPIO Zero](http://gpiozero.readthedocs.io/). See [People in Space Indicator](https://www.raspberrypi.org/learning/people-in-space-indicator/).
