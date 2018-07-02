import treq
from twisted.internet import reactor
import time

URL = "http://localhost:8888/files/"
FNAME = "downloaded"


def download_file(reactor, url, destination_filename):

    print "START TIME:", time.ctime()
    destination = open(destination_filename, 'wb')
    d = treq.get(url)
    d.addCallback(treq.collect, destination.write)
    d.addBoth(lambda _: destination.close())
    d.addBoth(end)

    return d

def end(_):
    
    print "END TIME:", time.ctime()

    reactor.stop()


def main():

    reactor.callWhenRunning(download_file, reactor, URL, FNAME)

    reactor.run()

if __name__ == '__main__':

    main()

