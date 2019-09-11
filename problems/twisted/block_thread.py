from twisted.internet import reactor

def sleep_for(seconds):
    """ Sleep for specified number of seconds
        Then print duration of sleep """

    import time
    time.sleep(seconds)
    print seconds, "seconds have passed"

def main():
    """ Call sleep function with different arguments in threads """
    reactor.callInThread(sleep_for, 2)
    reactor.callInThread(sleep_for, 1)
    reactor.callInThread(sleep_for, 3)

    reactor.callLater(4,reactor.stop)
    reactor.run()

if __name__ == '__main__':
    main()
