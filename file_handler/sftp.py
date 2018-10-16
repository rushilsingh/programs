from sys import stdout

from twisted.python.log import startLogging, err

from twisted.internet import reactor
from twisted.internet.defer import Deferred

from twisted.conch.ssh.common import NS
from twisted.conch.scripts.cftp import ClientOptions
from twisted.conch.ssh.filetransfer import FileTransferClient
from twisted.conch.client.connect import connect
from twisted.conch.client.default import SSHUserAuthClient, verifyHostKey
from twisted.conch.ssh.connection import SSHConnection
from twisted.conch.ssh.channel import SSHChannel


class SFTPSession(SSHChannel):

    def channelOpen(self, whatever):
        d = self.conn.sendRequest(
            self, 'subsystem', NS('sftp'), wantReply=True)
        d.addCallbacks(self._cbSFTP)

    def _cbSFTP(self, result):
        client = FileTransferClient()
        client.makeConnection(self)
        self.dataReceived = client.dataReceived
        self.conn._sftp.callback(client)


class SFTPConnection(SSHConnection):
    def serviceStarted(self):
        self.openChannel(SFTPSession())


def sftp(user, host, port):
    options = ClientOptions()
    options['host'] = host
    options['port'] = port
    conn = SFTPConnection()
    conn._sftp = Deferred()
    auth = SSHUserAuthClient(user, options, conn)
    connect(host, port, options, verifyHostKey, auth)
    return conn._sftp


def transfer(client):
    d = client.makeDirectory('foobarbaz', {})
    def cbDir(ignored):
        print 'Made directory'
    d.addCallback(cbDir)
    return d


class SFTP(object):

    @classmethod
    def get(cls, user, password, host, port=22, from_path=""):
        d = sftp(user, host, port)
        d.addCallback(transfer)
        d.addErrback(err, "Problem with SFTP transfer")
        d.addCallback(lambda ignored: reactor.stop())
