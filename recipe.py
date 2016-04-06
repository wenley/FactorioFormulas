
import yaml
import numbers

from util import format_amount

class RecipeBuilder(object):
  def __init__(self, arg=None):
    self.name = None
    self.inputs = None
    self.time = 0
    self.amount = 0
    self.buildings = 1

    if isinstance(arg, Recipe):
      recipe = arg

      self.name = recipe.name
      self.inputs = recipe.inputs
      self.time = recipe.time
      self.amount = recipe.amount
      self.buildings = recipe.buildings
    elif isinstance(arg, basestring):
      self.name = arg

  def with_name(self, name):
    self.name = name
    return self
  def with_inputs(self, inputs):
    self.inputs = inputs
    return self
  def with_time(self, time):
    self.time = time
    return self
  def with_amount(self, amount):
    self.amount = amount
    return self
  def with_buildings(self, buildings):
    self.buildings = buildings
    return self

  def build(self):
    return Recipe(self.name,
        self.inputs,
        self.time,
        self.amount,
        self.buildings)

class Recipe(object):
  def __init__(self, name, inputs, time, amount, buildings=1):
    self.name = name
    self.inputs = inputs
    self.time = time
    self.amount = amount
    self.buildings = buildings

  def __repr__(self):
    inputs = ", ".join("%d %s" % (amount, item) for item, amount in self.inputs.iteritems())

    return "%s %s = %s + %s ticks across %s buildings" % \
        (format_amount(self.amount), self.name, inputs, self.time, format_amount(self.buildings))

  def __mul__(self, num):
    if not isinstance(num, numbers.Number):
      raise TypeError('Recipes can only be multiplied by numbers')

    scale = float(num)

    return RecipeBuilder(self.name) \
        .with_inputs({ item: amount * scale for item, amount in self.inputs.iteritems() }) \
        .with_time(self.time) \
        .with_amount(self.amount * scale) \
        .with_buildings(self.buildings * scale) \
        .build()

  def scale_ticks(self, new_time):
    '''
    Adjust building count to produce same output given the new time constraint.
    '''
    scale = float(self.time) / new_time

    return RecipeBuilder(self) \
        .with_time(new_time) \
        .with_buildings(self.buildings * scale) \
        .build()

  def normalize(self):
    '''
    Adjust the recipe to use an integer number of buildings.
    '''
    pass

def load_data(file_name='recipes.yaml'):
  with open(file_name, 'r') as f:
    return yaml.safe_load(f)

def load_recipes_from_data(data):
  def recipe_from_name_and_factors(name, factors):
    return Recipe(name,
        factors['inputs'],
        factors.get('time', 1),
        factors.get('amount', 1))

  return [recipe_from_name_and_factors(name, factors) for name, factors in data.iteritems()]

recipes = load_recipes_from_data(load_data())
def recipe_for_item(item_name):
  global recipes
  try:
    return next(recipe for recipe in recipes if recipe.name == item_name)
  except StopIteration:
    return None

if __name__ == '__main__':
  r = recipes[0]

  print r
  print r.scale_ticks(1.5)
