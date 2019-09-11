def world():
    print "World"

def hello():
    print "Hello"

def exclaim():
    print "!"

def main():
    from twisted.internet import reactor

    reactor.callLater(4, reactor.stop)
    reactor.callLater(3, exclaim)
    reactor.callLater(2, world)
    reactor.callLater(1, hello)

    reactor.run()

if __name__ == '__main__':
    main()

