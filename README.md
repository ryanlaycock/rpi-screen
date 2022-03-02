# RPI Screen

## About

Raspberry Pi setup and project code for my 16x16 Pimoroni Unicorn HD LED RGB Matrix - acting as a PC monitor/display.

### Hardware

This project is using a [**RPI Zero WH**](https://www.raspberrypi.com/products/raspberry-pi-zero-w) and a 
[**Pimoroni Unicorn HAT HD**](https://shop.pimoroni.com/products/unicorn-hat-hd) directly connected to the pi's GRIO pins.

The Pi and display are then inside my [**LIAN LI Q58 case**](https://lian-li.com/product/q58/), behind the tempered glass panel.

The Pi is connected over USB to the PC as a USB Ethernet/RNDIS Gadget - therefore sharing an internet connection from the PC. 
The advantage this gives is the Pi doesn't need to be concerned about setting an internet connection to work, and can be accessed from the PC
like `rpiscreen.local` (or whatever the Pi's hostname is).

## Setup

- [Setting up the RPi as a network gadget](/setup/rpisetup.md)

## Projects
In this repo you can find multiple projects that can be configured to run on the display. The main program can be configured to show differnet 'projects' depending on conditions, such as clock when the attached PC is not under load, and CPU & GPU metrics when it is.

### Clock
The [Clock Project](/clock/) adds a clock frame, with the 24 hour time displayed in the centre, with seconds going around the edge of the display - making for a nice digital clock effect.

### Open Hardware Monitor
The [Open Hardware Monitor Project](/hwmonitor/) adds a CPU and GPU load and temperature readout, from a PC running [Open Hardware Monitor](https://openhardwaremonitor.org/). See the detailed [docs](/hwmonitor/README.md) for more information on how to configure this in this application, but also on the PC to get measurements from.

## TODO

### Project Ideas
- [ ] Weather monitor

### General
- [ ] Improve setup of configs

