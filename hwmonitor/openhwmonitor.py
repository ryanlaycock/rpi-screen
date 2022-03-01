#!/usr/bin/env python

import math
import requests
import json
import time
from common.digits import * 

metric_options = {
  0: "cpu_load",
  1: "cpu_temp",
  2: "gpu_load",
  3: "gpu_temp"
}

def add_open_hw_monitor_to_frame(min_temp, config, now, rgb, frame):
  try:  
    data = get_open_hw_monitor_json(config['addr'])
  except:
    return (False, frame)
  # check data if right temp

  cpu_temp = get_value_from_open_hw_monitor(data, config['cpu']['temp_id'])
  print(cpu_temp)

  if float(min_temp) > float(cpu_temp):
    return (False, frame)

  frame = render_frame(cpu_temp, "CPU", rgb, frame)
  time.sleep(1)
  return (True, frame)

  # check for right type - WIP so just CPU temp
  if now.second <= 20:
    metric_opt = math.floor(now.second/5)
  elif now.second <= 40:
    metric_opt = math.floor(now.second/10)
  else:
    metric_opt = math.floor(now.second/21)

# header must be 3 chars
def render_frame(value, header, rgb, frame):
  add_digit_to_frame(1, 10, letters_medium[header[0]], rgb, frame)
  add_digit_to_frame(6, 10, letters_medium[header[1]], rgb, frame)
  add_digit_to_frame(11, 10, letters_medium[header[2]], rgb, frame)

  pixel_x = 0
  y = 2
  for digit in value[:4]: # take first 4 max chars of value - TODO does this panic?
    if digit == ".":
      frame.add_pixel(pixel_x-1, y, rgb)
      continue

    add_digit_to_frame(pixel_x, y, numbers[digit], rgb, frame)
    pixel_x += 4          

  add_digit_to_frame(pixel_x, y+1, degrees_c, rgb, frame)
  return frame

def get_open_hw_monitor_json(addr):
  r = requests.get(addr, timeout=0.5)
  return r.json()

def get_value_from_open_hw_monitor(data, data_ids):
  final_child = get_final_child([data], data_ids[:-1])
  value = final_child[0]['Value']
  value = value.replace(" °C", "").replace(" %", "")  

  return value

def get_final_child(data, data_ids):
  next_child = data
  for data_id in data_ids:
    next_child = get_child(next_child, data_id)
  return next_child

def get_child(children, target_child_id):
  for child in children:
    if child['id'] == target_child_id:
      return child['Children']
