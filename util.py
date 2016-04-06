
import math

raws = [
  'iron',
  'iron_ore',
  'copper',
  'copper_ore',
  'water_units',
  'pgas',
  'coal',
  'alient_artifact',
]

def is_raw(item):
  return item in raws

def format_amount(amount):
  rounded = math.ceil(amount)
  if rounded == amount:
    return "%d" % (amount,)
  else:
    return "%d (%.2f)" % (rounded, amount)
