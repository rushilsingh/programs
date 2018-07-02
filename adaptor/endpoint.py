class Endpoint(object):

    def __init__(self, ip, port, end_type, cred, version):
        self.ip, self.port = ip, port
        self.type = end_type
        self.cred, self.version = cred, version
