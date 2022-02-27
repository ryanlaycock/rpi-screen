#!/usr/bin/env python

import unicornhathd
from datetime import datetime
import time

print("Running clock on rpi-screen")

unicornhathd.rotation(180)
unicornhathd.brightness(0.7)

rgb = [4, 161, 48] # Colour of PC components


numbers = {
  "1": [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[1,1,0],[0,1,0]],
  "2": [[1,1,1],[1,0,0],[0,1,0],[0,0,1],[1,0,1],[1,0,1],[0,1,0]],
  "3": [[0,1,0],[1,0,1],[0,0,1],[0,1,0],[0,0,1],[1,0,1],[0,1,0]],
  "4": [[0,0,1],[0,0,1],[0,0,1],[1,1,1],[1,0,1],[0,1,1],[0,0,1]],
  "5": [[0,1,0],[1,0,1],[0,0,1],[0,0,1],[1,1,0],[1,0,0],[1,1,1]],
  "6": [[0,1,0],[1,0,1],[1,0,1],[1,1,0],[1,0,0],[1,0,1],[0,1,0]],
  "7": [[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,0,1],[0,0,1],[1,1,1]],
  "8": [[0,1,0],[1,0,1],[1,0,1],[0,1,0],[1,0,1],[1,0,1],[0,1,0]],
  "9": [[0,0,1],[0,0,1],[0,0,1],[0,1,1],[1,0,1],[1,0,1],[0,1,0]],
  "0": [[0,1,0],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[0,1,0]]
}

def set_digit(start_x, start_y, digit):
  y = start_y
  for row in digit:
    x = start_x
    for column in row:
      if column: 
        unicornhathd.set_pixel(x, y, rgb[0], rgb[1], rgb[2])
      x += 1
    y += 1

def second_to_pixel(t, r, g, b):
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

  unicornhathd.set_pixel(x, y, r, g, b)
 

try:
  while True:
    now = datetime.now()
    unicornhathd.clear()

    # Time has changed so draw the new digits
    last_time = now.strftime('%H:%M')
    hour = now.strftime('%H')
    minute = now.strftime('%M')
    set_digit(1, 5, numbers[hour[0]])
    set_digit(4, 5, numbers[hour[1]])
    set_digit(9, 5, numbers[minute[0]])
    set_digit(12, 5, numbers[minute[1]])
    
    for i in range(0, now.second): 
      # add a dot for each second so far
      second_to_pixel(i, 0, 40, 11)
    
    unicornhathd.show()
    time.sleep(0.1)
  
except KeyboardInterrupt:
  unicornhathd.off()
