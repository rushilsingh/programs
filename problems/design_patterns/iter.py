class Iterator(object):

    def __init__(self, data):
        self.data = data
        self.counter = 0

    def __iter__(self):
        return self

    def next(self):
        if self.counter>=len(self.data):
            raise StopIteration

        while self.counter<len(self.data):
            self.counter+=1
            return self.data[self.counter-1]
