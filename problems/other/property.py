class Person(object):
    def __init__(self):
        self._name = None

    def get_name(self):
        print "Getting name..."
        return self._name

    def set_name(self, value):
        print "Setting name..."
        self._name = value

    def del_name(self):
        print "Deleting name..."
        del self._name

    name = property(get_name, set_name, del_name,
                   "I am the name property!")
