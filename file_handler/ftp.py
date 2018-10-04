# Twisted imports
from twisted.protocols.ftp import FTPClient, FileConsumer
from twisted.internet.protocol import ClientCreator
from twisted.internet import reactor, defer
import time


class FTP(object):


    @classmethod
    @defer.inlineCallbacks
    def get(cls, user, password, host, port, from_path):
        status = None

        try:
            #Set default port
            if port is None:
                port = 21

            # Connect to FTP server
            creator = ClientCreator(reactor, FTPClient, user, password, passive=0)
            ftp_client = yield creator.connectTCP(host, port)
            # Create a file handler to retrieve the file
            with open(from_path, "w") as file_object:
                consumer = FileConsumer(file_object)
                result = yield ftp_client.retrieveFile(from_path, consumer)
                for r in result:
                    if not r[0]:
                        status = "Error while retrieving file from FTP {}@{}:{}".format(user, host, port)
                        break

        except Exception as e:
            status = "Error while retrieving file from FTP {}@{}:{} due to {}".format(user, host, port, e.message)
        finally:
            reactor.stop()

        defer.returnValue(status)

if __name__ == '__main__':
    reactor.callWhenRunning(FTP.get, "username", "password", "172.23.106.217", None, "large_file")
    reactor.run()
