f
rom twisted.internet import reactor, defer


def get_deferred(value, delay):
    """ Returns a deferred that is called with
        specified value after specified delay """

    d = defer.Deferred()
    reactor.callLater(delay, d.callback, value)
    return d

@defer.inlineCallbacks
def triple(value, delay):
    """ Triple value returned by deferred
        and print using inline callbacks """

    temp = yield get_deferred(value, delay)
    result = 3*temp
    defer.returnValue(result)

@defer.inlineCallbacks
def print_triple(value, delay):
    """ Print triple of a value after a delay
        using deferred and inline callbacks.
        Stop reactor when finished """

    print "Value:", value, "Delay:", delay
    result = yield triple(value, delay)
    print "Result:", result
    reactor.stop()

def main():

    print_triple(3,3)
    reactor.run()

if __name__ == '__main__':
    main()
