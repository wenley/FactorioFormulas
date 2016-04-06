
import sys

from collections import defaultdict

from recipe import Recipe, recipe_for_item
from util import is_raw, format_amount

class Formula(object):
  def __init__(self, item, amount=1, ticks=1):
    self.machines = defaultdict(lambda: 0)
    self.raws = defaultdict(lambda: 0)
    self.ticks = ticks

    self.start_item = item
    self.start_amount = amount

    # This is the target that needs to be reached in the specified time frame
    self.inputs = [(item, amount)]
    self.expanded = False

  def __repr__(self):
    if not self.expanded:
      return "(Unexpanded) %d %s in %d ticks" % (self.start_amount, self.start_item, self.ticks)

    output = ["For %d %s in %d ticks:" % (self.start_amount, self.start_item, self.ticks)]

    if len(self.machines) > 0:
      machines = '\n'.join("%s %s" % (format_amount(amount), item) for item, amount in self.machines.iteritems())
      output.append("Machines:")
      output.append(machines)

    if len(self.raws) > 0:
      raws = '\n'.join("%s %s" % (format_amount(amount), item) for item, amount in self.raws.iteritems())
      output.append("Raws:")
      output.append(raws)

    return '\n'.join(output)

  def expand(self):
    # No more formulas to expand
    if len(self.inputs) == 0:
      self.expanded = True
      return

    # Pluck out one formula
    item, amount = self.inputs.pop()

    if is_raw(item):
      self.raws[item] += amount
    else:
      recipe = recipe_for_item(item)

      if recipe is None:
        print >> sys.stderr, "Sorry, could not find recipe for non-raw %s" % (item,)
        self.raws[item] += amount
        return self.expand()

      # Adjust building count based on the time allotted
      recipe = recipe.scale_ticks(self.ticks)

      # If the recipe builds more than needed,
      # scaling_factor should be < 1
      scaling_factor = float(amount) / recipe.amount

      expanded = recipe * scaling_factor

      self.machines[expanded.name] += expanded.buildings

      for item, amount in expanded.inputs.iteritems():
        self.inputs.append((item, amount))

    self.expand()

