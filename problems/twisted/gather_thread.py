from twisted.internet import reactor, defer, threads
from time import sleep

def sleep_for(seconds):
    """ Sleep for specified seconds
        Return number of seconds of sleep """

    sleep(seconds)
    return seconds


def wake_up(seconds):
    print "I'm done sleeping for", seconds, "seconds"

def stop(_):
    reactor.stop()

def main():
    """ Defer functions to threads
        Add deferreds to list
        Stop reactor once deferreds return """
    d1 = threads.deferToThread(sleep_for, 2)
    d2 = threads.deferToThread(sleep_for, 1)

    d1.addCallback(wake_up)
    d2.addCallback(wake_up)

    gathered = defer.gatherResults([d1,d2])
    gathered.addCallback(stop)

    reactor.run()

if __name__ == '__main__':
    main()
