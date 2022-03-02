#!/usr/bin/env python

import unicornhathd
from datetime import datetime
import logging
import time
import json
from clock.clock import *
from hwmonitor.openhwmonitor import *


class RPIScreen():
  def __init__(self, config_file_dir):
    try:
      with open(config_file_dir, 'r') as f:
        config = json.load(f)
        logging.info('Loaded config: %s', json.dumps(config))
    except Exception as e:
      logging.error('Could not read config file: %s: %s', config_file_dir, e)
      exit(1)

    try:
      self.brightness = config['brightness']
      self.rotation = config['rotation']
      self.red = config['red']
      self.green = config['green']
      self.blue = config['blue']
      self.open_hardware_monitor_config = config['open_hardware_monitor_config']
    except:
      logging.error('Missing config vars')
      exit(1)

    unicornhathd.rotation(self.rotation)
    unicornhathd.brightness(self.brightness)


  def get_rgb(self):
    return (self.red, self.green, self.blue)

  def get_open_hw_monitor_config(self):
    return (self.open_hardware_monitor_config)


  def update_frame(self, frame):
    """Frame should be a 16x16 2d array of tuples of 3 for (r,g,b). frame[0,0] is bottom left of the display"""
    unicornhathd.clear()
    for row_i, row in enumerate(frame):
      for col_i, col in enumerate(row):
        unicornhathd.set_pixel(row_i, col_i, col[0], col[1], col[2])
    unicornhathd.show()
    time.sleep(1/60) # 1/60 of a second ~= Max 60 fps


  def off(self):
    unicornhathd.off()
       

class Frame():
  def __init__(self):
    row = [(0,0,0)]*16
    self.frame = [[(0,0,0) for x in range(16)] for y in range(16)]

  
  def add_pixel(self, x, y, rgb):
    self.frame[x][y] = rgb 


  def to_2d_array(self):
    return self.frame

logging.basicConfig(level=logging.DEBUG)
rps = RPIScreen('/home/pi/github.com/ryanlaycock/rpi-screen/config/config.json') # TODO improve

try:
  while True:
    now = datetime.now()
    frame = Frame()
    result = (False, frame)

    try:
      result = add_open_hw_monitor_to_frame(rps.get_open_hw_monitor_config(), now, rps.get_rgb(), frame)
    except:
      logging.info("Could not get open HW frame")

    if result[0]: # Open HW Monitor frame successfully added
      rps.update_frame(result[1].to_2d_array())
      time.sleep(1) # Sleep longer here not to spam open hardware/PC    
    else: # Default to clock
      frame = add_clock_to_frame(now, rps.get_rgb(), frame)
      rps.update_frame(frame.to_2d_array())
      time.sleep(0.1)

except KeyboardInterrupt:
  rps.off()

