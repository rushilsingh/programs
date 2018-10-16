import cyclone.web
from twisted.internet import reactor, defer
from twisted.python import log
import sys
from endpoint import Endpoint
from endpoints.ssh.ssh import SSH
from endpoints.snmp.snmp import SNMP
from endpoints.rest.rest import REST
from api_exception import APIException
import json


class APIHandler(cyclone.web.RequestHandler):

    def get(self, *arg):

        response = self.handle_errors(
            "Method not allowed: No methods are allowed on this resource")
        return response

    def post(self, *arg):

        response = self.handle_errors(
            "Method not allowed: No methods are allowed on this resource")
        return response

    def put(self, *arg):

        response = self.handle_errors(
            "Method not allowed: No methods are allowed on this resource")
        return response

    def delete(self, *arg):

        response = self.handle_errors(
            "Method not allowed: No methods are allowed on this resource")
        return response

    def handle_errors(self, response):
        """ Set status code according to response """

        if type(response) is str:  # String indicates error
            err = APIException(response)
            response = {"message": response}
            self.send_error(err.code, reason=response)
        else:
            self.set_status(200)
            self.write(response)
            self.finish()

        return response

    def write_error(self, status_code, **kwargs):

        response = kwargs['reason']
        self.write(response)
        self.finish()

    def get_protocol(self, ip):
        """ Create endpoint from arguments in URI. Validate endpoint.
            Create protocol object from endpoint. Return errors as string
        """

        if "?port" in self.request.uri:
            port = int(self.get_argument("port"))
        else:
            port = None

        try:
            endpoint_type = self.get_argument("type")
            cred = self.get_argument("credentials")
            version = self.get_argument("version")
        except:
            return "Bad request: Malformed request"

        endpoint = Endpoint(ip, port, endpoint_type, cred, version)

        Protocol = {
            "snmp": SNMP,
            "ssh": SSH,
            "rest": REST
        }.get(endpoint_type, None)

        if not Protocol:
            return "Bad request: Endpoint not supported"
        try:
            protocol = Protocol(endpoint)
        except Exception, e:
            return e.message
        else:
            return protocol


class SysConfigHandler(APIHandler):

    @defer.inlineCallbacks
    def get(self, ip):

        # Get arguments from URL
        if not ip:
            response = "Bad request: No IP address provided"
        else:
            # Create protocol object
            protocol = self.get_protocol(ip)
            if type(protocol) is str:  # String indicates error
                response = protocol
            else:
                try:
                    response = yield protocol.get("sysconfig")
                except Exception, e:
                    response = e.message

        response = self.handle_errors(response)
        defer.returnValue(response)

    def post(self, *arg):

        response = self.handle_errors(
            "Method not allowed: Only GET is allowed for this resource")
        return response

    def put(self, *arg):

        response = self.handle_errors(
            "Method not allowed: Only GET is allowed for this resource")
        return response

    def delete(self, *arg):

        response = self.handle_errors(
            "Method not allowed: Only GET is allowed for this resource")
        return response


class DockerHandler(APIHandler):

    @defer.inlineCallbacks
    def get(self, ip, container_id):

        protocol = self.get_protocol(ip)

        if type(protocol) is str:
            response = protocol
        else:
            try:
                if not container_id:
                    response = protocol.list("docker")
                else:
                    response = yield protocol.get("docker", container_id)
            except Exception, e:
                response = e.message

        response = self.handle_errors(response)

        defer.returnValue(response)

    def post(self, ip, *args):

        protocol = self.get_protocol(ip)

        if type(protocol) is str:
            response = protocol
        else:
            try:
                json_data = json.loads(self.request.body)
                image = json_data.pop("Image", None)
                if not image:
                    response = "Bad request: Image not provided"
                else:
                    command = []
                    if "Name" in json_data:
                        command.append("--name=" + json_data["Name"])
                        # additional arguments for "docker run -d" can be handled here if needed

                    command.append(image)
                    command = tuple(command)

                    response = protocol.post("docker", *command)

            except ValueError, ve:
                response = "Internal server error: Error loading json. Message: " + ve.message

            except Exception, e:
                response = e.message

        response = self.handle_errors(response)
        return response

    def delete(self, ip, container_id):

        if not container_id:
            response = "Bad request: Container Id not provided"
        else:
            protocol = self.get_protocol(ip)

            if type(protocol) is str:
                response = protocol
            else:
                try:
                    response = protocol.delete("docker", container_id)
                except Exception, e:
                    response = e.message

        response = self.handle_errors(response)
        return response

    def put(self, *arg):

        response = self.handle_errors(
            "Method not allowed: GET, LIST, POST and DELETE are allowed for this resource")
        return response


if __name__ == "__main__":
    application = cyclone.web.Application(
        [(r"/api/v1/sysconfig/(.*)", SysConfigHandler),
         (r"/api/v1/docker/(.*)/containers/(.*)", DockerHandler),
         (r"/api/v1/(.*)", APIHandler)])

    log.startLogging(sys.stdout)
    reactor.listenTCP(8888, application)
    reactor.run()
