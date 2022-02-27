#!/usr/bin/env python

import unicornhathd
from datetime import datetime
import logging
import time
import json


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
      self.open_hardware_monitor_addr = config['open_hardware_monitor_addr']
    except:
      logging.error('Missing config vars')
      exit(1)

    unicornhathd.rotation(self.rotation)
    unicornhathd.brightness(self.brightness)


  def get_rgb(self):
    return (self.red, self.green, self.blue)


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
    self.frame[y][x] = rgb 


  def to_2d_array(self):
    return self.frame

logging.basicConfig(level=logging.DEBUG)
rps = RPIScreen('config/config.json')
try:
  while True:
    frame = Frame()
    frame.add_pixel(0, 0, rps.get_rgb())
    rps.update_frame(frame.to_2d_array())

except KeyboardInterrupt:
  rps.off()
