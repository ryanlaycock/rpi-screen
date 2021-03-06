#!/usr/bin/env python

import unicornhathd
from datetime import datetime
import time
from common.digits import *

def add_second_to_frame(t, rgb, frame):
  x = 0;
  y = 0;
  if t < 8: # 0-7
    x = 8 + t
    y = 15
  elif t > 7 and t < 23: # 8-22
    x = 15
    y = 22 - t
  elif t > 22 and t < 38: # 23-37
    x = 37 - t
    y = 0
  elif t > 37 and t < 53: # 38 - 52
    x = 0
    y = t - 37
  elif t > 52 and t < 60: # 53 - 59
    x = t - 52 
    y = 15

  frame.add_pixel(x, y, rgb) 

def add_clock_to_frame(now, rgb, frame):
  hour = now.strftime('%H')
  minute = now.strftime('%M')
  add_digit_to_frame(1, 5, numbers[hour[0]], rgb, frame)
  add_digit_to_frame(4, 5, numbers[hour[1]], rgb, frame)
  add_digit_to_frame(9, 5, numbers[minute[0]], rgb, frame)
  add_digit_to_frame(12, 5, numbers[minute[1]], rgb, frame)

  for i in range(0, now.second): 
    # add a dot for each second so far
    add_second_to_frame(i, rgb, frame)
    
  return frame
