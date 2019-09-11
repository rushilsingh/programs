class Singleton(type):
    _instances = {}

    def __call__(cls, *a, **k):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*a, **k)
        return cls._instances[cls]

class World(object):

    __metaclass__ = Singleton
    def see(self):
        print "I see the world with id:", id(self)
