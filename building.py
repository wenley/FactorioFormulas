
from resource_flow import ResourceFlow

class FactoryNode(object):
    '''
    Abstract class for objects that can be included in a resource flow graph.
    '''
    def inputs(self):
        '''
        @return ResourceFlow
        '''
        pass

    def throughput(self):
        '''
        @return ResourceFlow
        '''
        pass

    def __or__(self, other):
        '''
        Joins two Factory Nodes in parallel

        @return FactoryNode
        '''
        return self + other

    def __add__(self, other):
        '''
        Joins two Factory Nodes in parallel

        @return FactoryNode
        '''
        return ParallelNode(buildings=[self, other])

    def __lt__(self, other):
        '''
        Given a < b, chain the result of b into a
        '''
        return SeriesNode(other, self)

    def __gt__(self, other):
        '''
        Given a > b, chain the result of a into b
        '''
        return SeriesNode(self, other)

# Decorator that can be applied to a Building
# Modifies its power consumption, speed, output, and pollution
class Module(object):
    pass

class Building(FactoryNode):
    def __init__(self, recipe, modules=[]):
        self.recipe = recipe
        self.modules = modules

    def with_modules(self, modules):
        self.modules = modules
        return self

    def inputs(self):
        base = ResourceFlow.from_dict(self.recipe.inputs)
        print "Base inputs:", base
        return reduce(lambda result, module: module.inputs(result), self.modules, base)

    def throughput(self):
        base_velocity = float(self.recipe.amount) / self.recipe.ticks
        base = ResourceFlow.from_dict({ self.recipe.name: base_velocity })

        return reduce(lambda result, module: module.throughput(result), self.modules, base)

class ParallelNode(FactoryNode):
    def __init__(self, buildings=[]):
        self.buildings = buildings

    def inputs(self):
        return reduce(lambda a, b: a + b, (b.inputs() for b in self.buildings), ResourceFlow())

    def throughput(self):
        return reduce(lambda a, b: a + b, (b.throughput() for b in self.buildings), ResourceFlow())

class SeriesNode(FactoryNode):
    def __init__(self, producer, consumer):
        '''
        @param producer : FactoryNode - the node that feeds its output to consumer
        @param consumer : FactoryNode - the node that gets some inputs from producer
        '''
        self.producer = producer
        self.consumer = consumer

    def inputs(self):
        return self.consumer.inputs() - self.producer.throughput() + self.producer.inputs()

    def throughput(self):
        result = self.consumer.throughput()

if __name__ == "__main__":
    from recipe import recipe_for_item

    gear = Building(recipe_for_item('gear'))
    print 'Gear:'
    print gear.inputs()
    print gear.throughput()

    double_gear = gear + gear
    print "\nDouble Gear:"
    print double_gear.inputs()
    print double_gear.throughput()

    transporter = Building(recipe_for_item('transporter'))
    full_transporter = gear > transporter

    print "\nTransporter:"
    print full_transporter.inputs()
    print full_transporter.throughput()


