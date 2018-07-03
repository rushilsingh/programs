import urllib2
import time
from twisted.internet import reactor, defer


CHUNK = 1024
FNAME = "downloaded"


def download(url):

    print "START TIME:", time.ctime()
    start = time.time()

    try:

        remote_resource = urllib2.urlopen(url)

        with open(FNAME, "wb") as f:

            while True:

                chunk = remote_resource.read(CHUNK)
                f.write(chunk)
                if not chunk:
                    break

        remote_resource.close()

    except Exception, e:
        response = (False, e.message)

    else:
        response = (True, None)

    if response[0]:
        print "Successfully downloaded file"
    else:
        print "Failed due to:", response[1]

    print "END TIME:", time.ctime()
    duration = time.time() - start

    print "Took", duration, "seconds"

    reactor.callFromThread(reactor.stop)
    return response


def main():

    reactor.callInThread(download, "http://localhost:8888/files/")
    reactor.run()


if __name__ == '__main__':

    main()
