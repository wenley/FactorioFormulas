
from collections import defaultdict

class ResourceFlow(defaultdict):
    def __init__(self):
        super(ResourceFlow, self).__init__(lambda: 0)

    @classmethod
    def from_dict(klass, d):
        result = klass()
        for item, amount in d.iteritems():
            result[item] += amount
        return result

    def __add__(self, other):
        result = ResourceFlow()
        for item, amount in self.iteritems():
            result[item] += amount
        for item, amount in other.iteritems():
            result[item] += amount
        return result

    def __sub__(self, other):
        result = ResourceFlow()
        for item, amount in self.iteritems():
            result[item] += amount
        for item, amount in other.iteritems():
            if result[item] < amount:
                raise ValueError('Would result in negative flow')
            else:
                result[item] -= amount
        return result

if __name__ == '__main__':
    a = ResourceFlow()
    a['iron'] = 2

    b = ResourceFlow()
    b['iron'] = 1

