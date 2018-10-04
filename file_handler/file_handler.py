from sftp import SFTP
from ftp import FTP
from twisted.internet import reactor, defer
import time


SUPPORTED_PROTOCOLS = {
    "sftp": SFTP,
    "ftp": FTP
}


class FileHandler(object):

    def __init__(self, url):
        # Example:
        #   sftp://<user>:<password>@<ip>:<port>/<file_path>
        #   ftp://<user>:<password>@<ip>:<port>/<file_path>
        self.url = url


    @defer.inlineCallbacks
    def get(self):
        print "START TIME", time.ctime()

        status = None
        proto_name, url = self.url.split("://", 1)

        #Validate protocol
        protocol = SUPPORTED_PROTOCOLS.get(proto_name, None)

        if protocol is None:
            status = "Unsupported protocol"
        else:
            url, path = url.split("/", 1)
            credentials, destination = url.rsplit("@",1)
            user, password = credentials.split(":", 1)
            if ":" in destination:
                host, port = destination.rsplit(":", 1)
            else:
                host, port = destination, None

            try:
                status = yield protocol.get(user, password, host, port, path)
            except Exception, e:
                status = e.message

        print "END TIME:", time.ctime()

        if status is None:
            print "Successfully retrieved file from {} {}@{}".format(proto_name.upper(), user, host)
        else:
            print status


if __name__ == '__main__':
    fh = FileHandler("sftp://username:password@localhost/Downloads/test.txt")
    reactor.callWhenRunning(fh.get)
    reactor.run()
