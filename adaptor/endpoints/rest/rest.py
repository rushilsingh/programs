import sys
sys.path.insert(0, "/home/username/programs")
from adaptor.protocol_handler import Protocol_Handler
import json


CONF = "./conf/rest.conf"


class REST(Protocol_Handler):

    def __init__(self, endpoint):

        self.ip = endpoint.ip
        if endpoint.port:
            self.port = endpoint.port
        else:
            self.port = 80
        self.credentials = endpoint.cred
        self.user, self.password = self.credentials.split(":")
        self.version = int(endpoint.version)
        if self.version != 1:
            raise Exception("Bad request: Version not supported")

        self.url = "http://"+self.ip+":"+str(self.port)+"/"

    def get(self, feature_name, *args):

        if feature_name != "sysconfig":
            raise Exception("Not supported: Rest endpoint does not support this feature")

        try:
            with open(CONF) as f:
                path = json.loads(f.read())[feature_name]["get"]["path"]

            path = self.url + path

            import requests

            result = requests.get(path)
            result = result.json()

        except Exception, e:
            return "Internal Server Error: "+e.message

        # Construct response
        response = {}
        response["properties"] = result
        response["version"] = self.version
        response["credentials"] = self.credentials
        return response

    def post(self, feature_name, *args):
        raise NotImplementedError(
            "Method not allowed: REST currently supports only GET")

    def put(self, feature_name, *args):
        raise NotImplementedError(
            "Method not allowed: REST currently supports only GET")

    def list(self, feature_name, *args):
        raise NotImplementedError(
            "Method not allowed: REST currently supports only GET")

    def delete(self, feature_name, *args):
        raise NotImplementedError(
            "Method not allowed: REST currently supports only GET")
