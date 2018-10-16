from cyclone import web
from twisted.internet import reactor
from twisted.python import log
import sys


def main():
    log.startLogging(sys.stdout)
    application = web.Application([
        (r"/files/(.*)", web.StaticFileHandler, {"path": "huge_file"}),
    ])

    reactor.listenTCP(8888, application)
    reactor.run()


if __name__ == '__main__':
    main()
