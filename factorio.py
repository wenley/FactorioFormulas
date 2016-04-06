
from optparse import OptionParser

from recipe import recipe_for_item
from formula import Formula

parser = OptionParser()

parser.add_option("-r", "--recipe", type="string", dest="recipe_requested",
    help="Item whose recipe to recite.")

parser.add_option("-b", "--build", type="string", dest="build_target",
    help="Item to determine build for.")
parser.add_option("-a", "--amount", type="float", dest="amount", default=1,
    help="Amount of the item being built. [default 1].")
parser.add_option("-t", "--time", type="float", dest="ticks", default=None,
    help="Number of ticks allowed per batch. Defaults to the recipe time.")

parser.add_option('-v', '--verbose', action="store_true", dest="debug",
    help="Turn on logging.")


if __name__ == '__main__':
  (options, args) = parser.parse_args()

  if options.recipe_requested is not None and options.build_target is not None:
    print "Cannot request recipe and build at the same time."
  elif options.recipe_requested is not None:
    recipe = recipe_for_item(options.recipe_requested)

    if recipe:
      print recipe
    else:
      print "Could not find recipe with name %s" % (options.recipe_requested,)
  elif options.build_target is not None:
    if options.ticks is None:
      options.ticks = recipe_for_item(options.build_target).time

    formula = Formula(options.build_target, amount=options.amount, time=options.ticks)
    formula.expand()
    print formula
