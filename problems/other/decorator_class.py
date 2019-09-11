class Decorator(object):

    def __init__(self, function):
        self.function = function

    def __call__(self, *a, **kw):
        print "I am decorating", self.function.__name__
        return self.function(*a, **kw)

@Decorator
def simple(*a, **kw):
    print "I am a simple function"
    print "I ran with arguments",a, kw


