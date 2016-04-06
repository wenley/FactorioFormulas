
from optparse import OptionParser

from recipe import recipe_for_item, recipes
from formula import Formula

parser = OptionParser()

parser.add_option('-l', '--list', action="store_true", dest="list_recipes",
    help="Print a list of recipes.")
parser.add_option('--tag', action="append", type="string", dest="tags", default=[],
    help="Only print recipes with the specified tag. Can be listed multiple times.")

parser.add_option("-r", "--recipe", type="string", dest="recipe_requested",
    help="Item whose recipe to recite.")

parser.add_option("-b", "--build", type="string", dest="build_target",
    help="Item to determine build for.")
parser.add_option("-a", "--amount", type="float", dest="amount", default=1,
    help="Amount of the item being built. [default 1].")
parser.add_option("-t", "--ticks", type="float", dest="ticks", default=None,
    help="Number of ticks allowed per batch. 1 tick = 0.5 sec. Defaults to the recipe time.")

parser.add_option('-v', '--verbose', action="store_true", dest="verbose",
    help="Turn on logging.")


if __name__ == '__main__':
  (options, args) = parser.parse_args()

  if options.list_recipes:
    for recipe in recipes:
      if all(map(lambda t: t in recipe.tags, options.tags)):
        line = [recipe.name]

        remaining_tags = set(recipe.tags) - set(options.tags)
        if remaining_tags and options.verbose:
          line.append("[%s]" % (",".join(remaining_tags),))
        print " ".join(line)
  elif options.recipe_requested is not None:
    recipe = recipe_for_item(options.recipe_requested)

    if recipe:
      print recipe
    else:
      print "Could not find recipe with name %s" % (options.recipe_requested,)
  elif options.build_target is not None:
    ticks = options.ticks or recipe_for_item(options.build_target).ticks

    formula = Formula(options.build_target, amount=options.amount, ticks=ticks)
    formula.expand()
    print formula
