class Accumulator(object):

    def __init__(self):
        self.total = 0

    def add(self, value):
        self.total += value

    def __call__(self):
        return self.total


