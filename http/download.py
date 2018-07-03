import urllib2
import time
from twisted.internet import reactor, defer


CHUNK = 1024
FNAME = "downloaded"


@defer.inlineCallbacks
def get_file(url):

    start = time.time()
    response = yield download(url)
    duration = time.time() - start

    if response[0]:
        print "Successfully downloaded file"
    else:
        print "Failed due to :", response[1]
    print "Took", duration, "seconds"

    defer.returnValue(response)


def download(url):

    d = defer.Deferred()

    try:
        remote_resource = urllib2.urlopen(url)
                
        with open(FNAME , "wb") as f:

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
    d.callback(response)
    
    return d

reactor.callWhenRunning(get_file, "http://localhost:8888/files/")

reactor.run()
