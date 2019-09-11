
class Employee(object):

    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)


    @fullname.setter
    def fullname(self, name):
        self.first, self.last = name.split(' ')


    @fullname.deleter
    def fullname(self):
        print 'Deleting name...'
        self.first = None
        self.last = None
