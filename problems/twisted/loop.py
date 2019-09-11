from twisted.internet import task
from twisted.internet import reactor
counter = 0

def run_frequently(frequency, times):
    """ Updates counter and prints value
        Stops reactor when counter exceeds limit """

    global counter

    if counter==0:
        print "I run every", frequency, "seconds"
        print "I will run", times, "times\n"
        counter += 1
    elif counter>times:
        print "Stopping.."
        reactor.stop()
    else:
        print "I have run", counter, "times"
        counter += 1


def create_loop(frequency, times):
    """ Create a looping call with specified frequency
        and for a specified number of times """

    l = task.LoopingCall(run_frequently, frequency, times)
    l.start(frequency)


def main():

    create_loop(1,10)
    reactor.run()

if __name__ == '__main__':
    main()

