from twisted.internet import reactor

class Counter(object):
    """ Counter class contains three counts that
        decrement at different rates """

    def __init__(self):
        """ Initialize counters """

        self.a = 5
        self.b = 10
        self.c = 15

    def check(self):
        """ If all counters are 0, stop reactor """
        if self.a == self.b == self.c == 0:
            print "Stopping..."
            reactor.stop()

    def count_a(self):
        """ Decrements a once per second """
        if self.a == 0:
            self.check()
        else:
            print self.a, "a"*5
            self.a -= 1
            reactor.callLater(1, self.count_a)

    def count_b(self):
        """ Decrements b once per 0.5 seconds """
        if self.b == 0:
            self.check()
        else:
            print self.b, "b"*5
            self.b -= 1
            reactor.callLater(0.5, self.count_b)

    def count_c(self):
        """ Decrements c once per 0.3 seconds """
        if self.c == 0:
            self.check()
        else:
            print self.c, "c"*5
            self.c -= 1
            reactor.callLater(0.3, self.count_c)

def main():

    c = Counter()
    reactor.callWhenRunning(c.count_a)
    reactor.callWhenRunning(c.count_b)
    reactor.callWhenRunning(c.count_c)

    print "Starting.."
    reactor.run()

if __name__ == '__main__':
    main()



