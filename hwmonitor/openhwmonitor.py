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

def add_open_hw_monitor_to_frame(config, now, rgb, frame):
  min_temp = config['min_temp']

  try:  
    data = get_open_hw_monitor_json(config['addr'])
  except:
    logging.info("Failed to get open_hw data", e)
    return (False, frame)

  cpu_temp = get_value_from_open_hw_monitor(data, config['cpu']['temp_id'])
  cpu_load = get_value_from_open_hw_monitor(data, config['cpu']['load_id'])
  gpu_temp = get_value_from_open_hw_monitor(data, config['gpu']['temp_id'])
  gpu_load = get_value_from_open_hw_monitor(data, config['gpu']['load_id'])

  if float(min_temp) > float(cpu_temp) or float(min_temp) > float(gpu_temp):
    logging.info("Open HW temps lower than threshold. CPU_TEMP %s, GPU_TEMP %s, MIN %s", str(cpu_temp), str(gpu_temp), str(min_temp))
    return (False, frame)

  if now.second < 20:
    metric_opt = metric_options[math.floor(now.second/5)]
  elif now.second < 40:
    metric_opt = metric_options[math.floor((now.second-20)/5)]
  else:
    metric_opt = metric_options[math.floor((now.second-40)/5)]

  if metric_opt == "cpu_load":
    return (True, render_frame(cpu_load, "CPU", percent, 0, rgb, frame))
  elif metric_opt == "cpu_temp":
    return (True, render_frame(cpu_temp, "CPU", degrees_c, 1, rgb, frame))
  elif metric_opt == "gpu_load":
    return (True, render_frame(gpu_load, "GPU", percent, 2, rgb, frame))
  elif metric_opt == "gpu_temp":
    return (True, render_frame(gpu_temp, "GPU", degrees_c, 3, rgb, frame))
  
  return (False, frame)

# header must be 3 chars
def render_frame(value, header, unit, frame_num, rgb, frame): # TODO improve frame_num & unit
  half_rgb = tuple(int(rgbi/2) for rgbi in rgb)
  add_digit_to_frame(1, 10, letters_medium[header[0]], half_rgb, frame)
  add_digit_to_frame(6, 10, letters_medium[header[1]], half_rgb, frame)
  add_digit_to_frame(11, 10, letters_medium[header[2]], half_rgb, frame)

  pixel_x = 0
  y = 2
  for digit in value[:4]:
    if digit == ".":
      frame.add_pixel(pixel_x-1, y, rgb)
      continue

    add_digit_to_frame(pixel_x, y, numbers[digit], rgb, frame)
    pixel_x += 4          

  add_digit_to_frame(pixel_x, y+1, unit, rgb, frame)

  for i in range(4):
    bottom_rgb = rgb
    if i != frame_num:
      bottom_rgb = half_rgb
    frame.add_pixel(3 + (i * 3), 0, bottom_rgb)
    
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
    if child['Text'] == target_child_id:
      return child['Children']
