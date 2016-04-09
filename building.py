
from collections import defaultdict

class FactoryNode(object):
    '''
    Abstract class for objects that can be included in a resource flow graph.
    '''
    def inputs(self):
        pass

    def throughput(self):
        pass

    def __or__(self, other):
        '''
        Joins two Factory Nodes in parallel
        '''
        return OrNode(buildings=[self, other])

    def __add__(self, next_node):
        '''
        Joins two Factory Nodes in series
        '''
        pass

# Decorator that can be applied to a Building
# Modifies its power consumption, speed, output, and pollution
class Module(object):
    pass

class Building(object):
    def __init__(self, level, recipe, modules=[]):
        self.recipe = recipe
        self.modules = modules

    def with_modules(self, modules):
        self.modules = modules
        return self

    def inputs(self):
        return reduce(lambda result, module: module.inputs(result), self.modules)

    def throughput(self):
        base = float(self.recipe.amount) / self.recipe.ticks
        return reduce(lambda result, module: module.throughput(result), self.modules)

class OrNode(object):
    def __init__(self, buildings=[]):
        self.buildings = []

    def inputs(self):
        result = defaultdict(lambda: 0.0)
        for b in buildings:
            ticks = b.ticks()
            for item, amount in b.inputs.iteritems():
                result[item] += amount
        return result

    def throughput(self):
        return sum(b.throughput() for b in buildings())

class AndNode(object):
    def __init__(self, producer, consumer):
        '''
        @param producer : FactoryNode - the node that feeds its output to consumer
        @param consumer : FactoryNode - the node that gets some inputs from producer
        '''
        self.producer = producer
        self.consumer = consumer

    def inputs(self):
        result = self.consumer.inputs()
        result[producer.recipe.name] -= producer.throughput()

        for item, amount in producer.inputs():
            result[item] += amount
        return result

    def throughput(self):
        result = self.producer.throughput()


