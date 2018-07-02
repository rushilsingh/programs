import unittest
from mock import patch
from mock import MagicMock
import sys
sys.path.insert(0, '/home/username/programs')
from adaptor import endpoint
from adaptor.api_handler import APIHandler, SysConfigHandler, DockerHandler
from adaptor.endpoints.snmp import snmp
from adaptor.endpoints.ssh import ssh
from cyclone.web import Application
from cyclone.httpserver import HTTPRequest
from twisted.internet import defer


class APIHandler_Tests(unittest.TestCase):

    def test_handle_errors_response_without_error(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/sysconfig/172.23.106.233?type=ssh&credentials=username:password&version=1')
        request.connection = MagicMock()  # mock connection
        handler = APIHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        response = {
            "credentials": "username:password",
            "version": 1,
            "properties": [{
                "Name": "ubuntu132",
                "Description": "64 bit system running 3.13.0-74-generic"
            }]
        }

        result = handler.handle_errors(response)
        expected_result = response  # Response should be unchanged

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 200)

    def test_handle_errors_response_with_error(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/sysconfig/172.23.106.233?type=ssh&credentials=username:password&version=1')
        request.connection = MagicMock()  # mock connection
        handler = APIHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        response = "Internal Server Error: Something went wrong"

        result = handler.handle_errors(response)

        expected_result = {"message": response}

        self.assertEquals(handler.get_status(), 500)
        self.assertEquals(result, expected_result)

    def test_get_protocol_valid_snmp_default_port(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/sysconfig/172.23.106.233?type=snmp&credentials=public:private&version=1')
        request.connection = MagicMock()  # mock connection
        handler = APIHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        protocol = handler.get_protocol("172.23.106.233")

        self.assertIsInstance(protocol, snmp.SNMP)
        self.assertEquals(protocol.target, ("172.23.106.233", 161))
        self.assertEquals(protocol.credentials, "public:private")
        self.assertEquals(protocol.version, 1)

    def test_get_protocol_valid_snmp_specified_port(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/sysconfig/172.23.106.233?port=161&type=snmp&credentials=public:private&version=1')
        request.connection = MagicMock()  # mock connection
        handler = APIHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        protocol = handler.get_protocol("172.23.106.233")

        self.assertIsInstance(protocol, snmp.SNMP)
        self.assertEquals(protocol.target, ("172.23.106.233", 161))
        self.assertEquals(protocol.credentials, "public:private")
        self.assertEquals(protocol.version, 1)

    def test_get_protocol_valid_ssh_default_port(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/sysconfig/172.23.106.233?type=ssh&credentials=username:password&version=1')
        request.connection = MagicMock()  # mock connection
        handler = APIHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        protocol = handler.get_protocol("172.23.106.233")

        self.assertIsInstance(protocol, ssh.SSH)
        self.assertEquals(protocol.ip, "172.23.106.233")
        self.assertEquals(protocol.port, 22)
        self.assertEquals(protocol.credentials, "username:password")
        self.assertEquals(protocol.version, 1)

    def test_get_protocol_valid_ssh_specified_port(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/sysconfig/172.23.106.233?port=22&type=ssh&credentials=username:password&version=1')
        request.connection = MagicMock()  # mock connection
        handler = APIHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        protocol = handler.get_protocol("172.23.106.233")

        self.assertIsInstance(protocol, ssh.SSH)
        self.assertEquals(protocol.ip, "172.23.106.233")
        self.assertEquals(protocol.port, 22)
        self.assertEquals(protocol.credentials, "username:password")
        self.assertEquals(protocol.version, 1)

    def test_get_protocol_invalid_malformed_request(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/sysconfig/172.23.106.233?port=22&type=ssh&credentials=username:password')
        request.connection = MagicMock()  # mock connection
        handler = APIHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        protocol = handler.get_protocol("172.23.106.233")
        self.assertEquals(protocol, "Bad request: Malformed request")

    def test_get_protocol_invalid_unsupported_endpoint(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/sysconfig/172.23.106.233?port=22&type=invalid&credentials=username:password&version=1')
        request.connection = MagicMock()  # mock connection
        handler = APIHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        protocol = handler.get_protocol("172.23.106.233")
        self.assertEquals(protocol, "Bad request: Endpoint not supported")

    def test_get_not_allowed(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/something')
        request.connection = MagicMock()  # mock connection
        handler = APIHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        result = handler.get("something")
        expected_result = {
            'message': 'Method not allowed: No methods are allowed on this resource'}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 405)

    def test_post_not_allowed(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'POST', '/api/v1/something')
        request.connection = MagicMock()  # mock connection
        handler = APIHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        result = handler.post("something")
        expected_result = {
            'message': 'Method not allowed: No methods are allowed on this resource'}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 405)

    def test_put_not_allowed(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'PUT', '/api/v1/something')
        request.connection = MagicMock()  # mock connection
        handler = APIHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        result = handler.delete("something")
        expected_result = {
            'message': 'Method not allowed: No methods are allowed on this resource'}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 405)

    def test_delete_not_allowed(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'DELETE', '/api/v1/something')
        request.connection = MagicMock()  # mock connection
        handler = APIHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        result = handler.get("something")
        expected_result = {
            'message': 'Method not allowed: No methods are allowed on this resource'}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 405)


class SysConfigHandler_Tests(unittest.TestCase):

    @defer.inlineCallbacks
    def test_sysconfig_get_snmp_valid(self):

        # patch snmp get method to return valid response
        snmp.SNMP.get = MagicMock(
            return_value={
                "credentials": "public:private", "version": 1,
                "properties": [{
                    "Location": "Alten Calsoft Labs",
                    "Description": "Linux CLPSTPDFC115 3.19.0-25-generic #26~14.04.1-Ubuntu SMP Fri Jul 24 21:16:20 UTC 2015 x86_64",
                    "Name": "CLPSTPDFC115"
                }]
            }
        )

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/sysconfig/127.0.0.1?type=snmp&credentials=public:private&version=1')
        request.connection = MagicMock()  # mock connection
        handler = SysConfigHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        # call handler's get method and validate result
        result = yield handler.get("sysconfig")
        expected_result = {
            'credentials': 'public:private', 'version': 1,
            'properties': [{
                'Name': 'CLPSTPDFC115', 'Location': 'Alten Calsoft Labs',
                'Description': 'Linux CLPSTPDFC115 3.19.0-25-generic #26~14.04.1-Ubuntu SMP Fri Jul 24 21:16:20 UTC 2015 x86_64'
            }]
        }

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 200)

    @defer.inlineCallbacks
    def test_sysconfig_get_snmp_invalid_version_not_supported(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/sysconfig/127.0.0.1?type=snmp&credentials=public:private&version=3')
        request.connection = MagicMock()  # mock connection
        handler = SysConfigHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        # call handler's get method and validate result
        result = yield handler.get("sysconfig")
        expected_result = {'message': 'Bad request: Version not supported'}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 400)

    @defer.inlineCallbacks
    def test_sysconfig_snmp_invalid_device_returned_error(self):

        # patch snmp get method to return error response
        snmp.SNMP.get = MagicMock(
            return_value="Internal Server Error: Something went wrong")

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', 'http://localhost:8888/api/v1/sysconfig/127.0.0.1?type=snmp&credentials=public:private&version=1')
        request.connection = MagicMock()  # mock connection
        handler = SysConfigHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        # call handler's get method and validate result
        result = yield handler.get("sysconfig")
        expected_result = {
            'message': 'Internal Server Error: Something went wrong'}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 500)

    @defer.inlineCallbacks
    def test_sysconfig_get_ssh_valid(self):

        # patch ssh get method to return valid response
        ssh.SSH.get = MagicMock(
            return_value={
                "credentials": "username:password", "version": 1,
                "properties": [{
                    "Name": "username", "Description": "64 bit system running 4.4.0-21-generic"
                }]
            }
        )

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/sysconfig/172.23.106.201?type=ssh&credentials=username:password&version=1')
        request.connection = MagicMock()  # mock connection
        handler = SysConfigHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        # call handler's get method and validate result
        result = yield handler.get("sysconfig")
        expected_result = {
            "credentials": "username:password", "version": 1,
            "properties": [{
                "Name": "username", "Description": "64 bit system running 4.4.0-21-generic"
            }]
        }

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 200)

    @defer.inlineCallbacks
    def test_sysconfig_get_ssh_invalid_version_not_supported(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/sysconfig/172.23.106.201?type=ssh&credentials=username:password&version=2')
        request.connection = MagicMock()  # mock connection
        handler = SysConfigHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        # call handler's get method and validate result
        result = yield handler.get("sysconfig")
        expected_result = {'message': 'Bad request: Version not supported'}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 400)

    @defer.inlineCallbacks
    def test_sysconfig_get_ssh_invalid_device_returned_error(self):

        # patch ssh get method to return error response
        ssh.SSH.get = MagicMock(
            return_value="Internal Server Error: Something went wrong")

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/sysconfig/172.23.106.201?type=ssh&credentials=username:password&version=1')
        request.connection = MagicMock()  # mock connection
        handler = SysConfigHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        # call handler's get method and validate result
        result = yield handler.get("sysconfig")
        expected_result = {
            'message': 'Internal Server Error: Something went wrong'}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 500)

    @defer.inlineCallbacks
    def test_sysconfig_get_invalid_endpoint_not_supported(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/sysconfig/172.23.106.201?type=invalid&credentials=username:password&version=1')
        request.connection = MagicMock()  # mock connection
        handler = SysConfigHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        # call handler's get method and validate result
        result = yield handler.get("sysconfig")
        expected_result = {'message': 'Bad request: Endpoint not supported'}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 400)

    def test_sysconfig_post_not_allowed(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'POST', '/api/v1/sysconfig/172.23.106.201')
        request.connection = MagicMock()  # mock connection
        handler = SysConfigHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        result = handler.post("172.23.106.201")

        expected_result = {
            'message': 'Method not allowed: Only GET is allowed for this resource'}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 405)

    def test_sysconfig_put_not_allowed(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'PUT', '/api/v1/sysconfig/172.23.106.201')
        request.connection = MagicMock()  # mock connection
        handler = SysConfigHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        result = handler.put("172.23.106.201")

        expected_result = {
            'message': 'Method not allowed: Only GET is allowed for this resource'}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 405)

    def test_sysconfig_delete_not_allowed(self):

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'DELETE', '/api/v1/sysconfig/172.23.106.201')
        request.connection = MagicMock()  # mock connection
        handler = SysConfigHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        result = handler.delete("172.23.106.201")

        expected_result = {
            'message': 'Method not allowed: Only GET is allowed for this resource'}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 405)


class DockerHandler_Tests(unittest.TestCase):

    @defer.inlineCallbacks
    def test_docker_get_ssh_valid(self):

        # patch ssh get method to return valid response
        ssh.SSH.get = MagicMock(
            return_value={
                "credentials": "username:password", "version": 1,
                "properties": [{
                    "Image": "95270569baf65db9449b7dff671b8f6c14af0c7c66cc220a1189c6915d33cb62",
                    "Id": "a1338284534e3e352bebdfbe7110a067c98e51575a8329482a5bba498785817f",
                    "Name": "trusting_hugle"
                }]
            }
        )

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/docker/172.23.106.217/containers/a1338284534e?type=ssh&credentials=username:password&version=1')
        request.connection = MagicMock()  # mock connection
        handler = DockerHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        result = yield handler.get("172.23.106.217", "a1338284534e")
        expected_result = {
            "credentials": "username:password", "version": 1,
            "properties": [{
                "Image": "95270569baf65db9449b7dff671b8f6c14af0c7c66cc220a1189c6915d33cb62",
                "Id": "a1338284534e3e352bebdfbe7110a067c98e51575a8329482a5bba498785817f",
                "Name": "trusting_hugle"
            }]
        }

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 200)

    @defer.inlineCallbacks
    def test_docker_get_ssh_invalid_device_returned_error(self):

        # patch ssh get method to return error response
        ssh.SSH.get = MagicMock(
            return_value="Internal Server Error: Something went wrong"
        )

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/docker/172.23.106.217/containers/a1338284534e?type=ssh&credentials=username:password&version=1')
        request.connection = MagicMock()  # mock connection
        handler = DockerHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        result = yield handler.get("172.23.106.217", "a1338284534e")
        expected_result = {
            'message': 'Internal Server Error: Something went wrong'}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 500)

    def test_docker_list_ssh_valid(self):

        # patch ssh list method to return valid response
        ssh.SSH.list = MagicMock(
            return_value={
                "credentials": "username:password", "version": 1,
                "properties": [
                    {
                        "Image": "24d48ae3a433",
                        "Container_Id": "63d3119cc589",
                        "Name": "nothing"
                    },
                    {
                        "Image": "24d48ae3a433",
                        "Container_Id": "3e1e69719464",
                        "Name": "something"
                    }
                ]
            }
        )

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/docker/172.23.106.217/containers/?type=ssh&credentials=username:password&version=1')
        request.connection = MagicMock()  # mock connection
        handler = DockerHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        result = yield handler.get("172.23.106.217", "")
        expected_result = {
            "credentials": "username:password", "version": 1,
            "properties": [
                {
                    "Image": "24d48ae3a433",
                    "Container_Id": "63d3119cc589",
                    "Name": "nothing"
                },
                {
                    "Image": "24d48ae3a433",
                    "Container_Id": "3e1e69719464",
                    "Name": "something"
                }
            ]
        }

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 200)

    def test_docker_list_ssh_invalid_device_returned_error(self):

        # patch ssh list method to return error response
        ssh.SSH.list = MagicMock(
            return_value="Internal Server Error: Something went wrong")

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/docker/172.23.106.217/containers/?type=ssh&credentials=username:password&version=1')
        request.connection = MagicMock()  # mock connection
        handler = DockerHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        result = yield handler.get("172.23.106.217", "")
        expected_result = {
            "message": "Internal Server Error: Something went wrong"}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 500)

    def test_docker_post_ssh_valid(self):

        # patch post method to return valid response
        ssh.SSH.post = MagicMock(
            return_value={
                "credentials": "username:password",
                "version": 1,
                "properties": [
                    {
                        "Container_Id": "568ce49d2cba715e91a355a2a4b96ddbeb3ac9cd7a6747aa207f30b4d0f15c6e"
                    }
                ]
            }
        )

        # instantiate a handler with a request object
        app = Application()

        request = HTTPRequest(
            method='POST',
            uri='/api/v1/docker/172.23.106.217/containers/?type=ssh&credentials=username:password&version=1',
            body='{"Image": "ubuntu", "Name": "another_example"}'
        )

        request.connection = MagicMock()  # mock connection
        handler = DockerHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        result = handler.post("172.23.106.217", "")

        expected_result = {
            "credentials": "username:password",
            "version": 1,
            "properties": [
                {
                    "Container_Id": "568ce49d2cba715e91a355a2a4b96ddbeb3ac9cd7a6747aa207f30b4d0f15c6e"
                }
            ]
        }

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 200)

    def test_docker_post_ssh_invalid_device_returned_error(self):

        # patch post method to return error response
        ssh.SSH.post = MagicMock(
            return_value="Internal Server Error: Something went wrong"
        )

        # instantiate a handler with a request object
        app = Application()

        request = HTTPRequest(
            method='POST',
            uri='/api/v1/docker/172.23.106.217/containers/?type=ssh&credentials=username:password&version=1',
            body='{"Image": "ubuntu", "Name": "another_example"}'
        )

        request.connection = MagicMock()  # mock connection
        handler = DockerHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        result = handler.post("172.23.106.217", "")

        expected_result = {
            "message": "Internal Server Error: Something went wrong"}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 500)

    def test_docker_delete_ssh_valid(self):

        # patch ssh get method to return valid response
        ssh.SSH.delete = MagicMock(
            return_value={
                "credentials": "username:password",
                "version": 1,
                "properties": [{
                    "Container": "a1338284534e"
                }]
            }
        )

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/docker/172.23.106.217/containers/a1338284534e?type=ssh&credentials=username:password&version=1')
        request.connection = MagicMock()  # mock connection
        handler = DockerHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        result = yield handler.delete("172.23.106.217", "a1338284534e")
        expected_result = {
            "credentials": "username:password",
            "version": 1,
            "properties": [{
                "Container": "a1338284534e"
            }]
        }

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 200)

    def test_docker_delete_ssh_invalid_device_returned_error(self):

        # patch ssh get method to return error response
        ssh.SSH.delete = MagicMock(
            return_value="Internal Server Error: Something went wrong"
        )

        # instantiate a handler with a request object
        app = Application()
        request = HTTPRequest(
            'GET', '/api/v1/docker/172.23.106.217/containers/a1338284534e?type=ssh&credentials=username:password&version=1')
        request.connection = MagicMock()  # mock connection
        handler = DockerHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        result = yield handler.delete("172.23.106.217", "a1338284534e")
        expected_result = {
            "message": "Internal Server Error: Something went wrong"}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 500)

    def test_docker_put_not_allowed(self):

        app = Application()
        request = HTTPRequest(
            'PUT', '/api/v1/docker/172.23.106.217/containers/a1338284534e?type=ssh&credentials=username:password&version=1')
        request.connection = MagicMock()  # mock connection
        handler = DockerHandler(app, request)

        handler.write = MagicMock()  # mock write
        handler.finish = MagicMock()  # mock finish

        result = handler.put("172.23.106.217", "a1338284534e")
        expected_result = {
            'message': 'Method not allowed: GET, LIST, POST and DELETE are allowed for this resource'}

        self.assertEquals(result, expected_result)
        self.assertEquals(handler.get_status(), 405)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
