class Person(object):
    def __init__(self):
        self._name = None

    @property
    def name(self):
        """I am the name property."""
        print "Getting name..."
        return self._name

    @name.setter
    def name(self, name):
        print "Setting name..."
        self._name = name

    @name.deleter
    def name(self):
        print "Deleting name..."
        del self._name
