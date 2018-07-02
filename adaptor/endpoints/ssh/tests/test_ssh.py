import unittest
from mock import patch
from mock import MagicMock
import sys
sys.path.insert(0, "/home/username/programs")
from adaptor import endpoint
from adaptor.endpoints.ssh import ssh
from spur.results import ExecutionResult

import json

docker_inspect_list = ["[", "{",
                       '    "Id": "a1338284534e3e352bebdfbe7110a067c98e51575a8329482a5bba498785817f",',
                       '    "Image": "95270569baf65db9449b7dff671b8f6c14af0c7c66cc220a1189c6915d33cb62",',
                       '    "Name": "/trusting_hugle",'
                       ]
docker_inspect_string = "\n".join(docker_inspect_list)


class SSH_Tests(unittest.TestCase):

    def setUp(self):
        ep = endpoint.Endpoint('172.23.106.201', 22,
                               'ssh', "username:password", 1)
        self.ssh = ssh.SSH(ep)

    def test_initialize_valid(self):

        ep = endpoint.Endpoint('172.23.106.201', 22,
                               'ssh', 'username:password', 1)

        try:
            ssh_obj = ssh.SSH(ep)
        except:
            self.fail("Failed to initialize object with valid parameters")

    def test_initialize_invalid_version(self):

        ep = endpoint.Endpoint('172.23.106.201', 22,
                               'ssh', 'username:password', 2)

        with self.assertRaises(Exception) as cm:
            ssh_obj = ssh.SSH(ep)

        self.assertEquals(cm.exception.message,
                          "Bad request: Version not supported")

    def test_sysconfig_get_parse_64_bit(self):
        data = [{
            "Name": "System Name",
            "Architecture": "x86_64",
            "Kernel": '3.19.0-25-generic'
        }]
        result = ssh.sysconfig_get_parse(data)
        expected_result = [{
            'Name': 'System Name',
            'Description': '64 bit system running 3.19.0-25-generic'
        }]
        self.assertEquals(result, expected_result)

    def test_sysconfig_get_parse_32_bit(self):
        data = [{
            "Name": "System Name",
            "Architecture": "i686",
            "Kernel": '3.19.0-25-generic'
        }]
        result = ssh.sysconfig_get_parse(data)
        expected_result = [{
            'Name': 'System Name',
            'Description': '32 bit system running 3.19.0-25-generic'
        }]
        self.assertEquals(result, expected_result)

    def test_sysconfig_get_parse_unknown_architecture(self):
        data = [{
            "Name": "System Name",
            "Architecture": "x11_11",
            "Kernel": '3.19.0-25-generic'
        }]
        result = ssh.sysconfig_get_parse(data)
        expected_result = [{
            'Name': 'System Name',
            'Description': 'Unknown processor running 3.19.0-25-generic'
        }]
        self.assertEquals(result, expected_result)

    def test_specific_parse_sysconfig_get(self):

        data = [{
            "Name": "System Name",
            "Architecture": "x86_64",
            "Kernel": '3.19.0-25-generic'
        }]
        result = self.ssh.specific_parse(data, "sysconfig_get")
        expected_result = [{
            'Name': 'System Name',
            'Description': '64 bit system running 3.19.0-25-generic'
        }]
        self.assertEquals(result, expected_result)

    def test_specific_parse_invalid_parser(self):

        data = [{
            "Name": "System Name",
            "Architecture": "x86_64",
            "Kernel": '3.19.0-25-generic'
        }]
        result = self.ssh.specific_parse(data, "invalid_parser")
        expected_result = [{
            "Name": "System Name",
            "Architecture": "x86_64",
            "Kernel": '3.19.0-25-generic'
        }]

        self.assertEquals(result, expected_result)

    def test_general_parse_with_sysconfig_valid(self):
        data = ("Linux CLPSTPDFC115 3.19.0-25-generic #26~14.04.1-Ubuntu SMP "
                + "Fri Jul 24 21:16:20 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux")
        result = self.ssh.general_parse(
            text=data, fsm="./conf/sysconfig_get.fsm")

        expected_result = [{
            'Kernel': '3.19.0-25-generic',
            'Name': 'CLPSTPDFC115',
            'Architecture': 'x86_64'
        }]
        self.assertEquals(result, expected_result)

    def test_general_parse_with_docker_list_valid(self):

        data = "'a1338284534e ubuntu trusting_hugle'\n'0a6692ebea53 95270569baf6 dreamy_roentgen'"

        result = self.ssh.general_parse(
            text=data, fsm="./conf/docker_list.fsm")

        expected_result = [
            {
                'Image': 'ubuntu', 'Container_Id': 'a1338284534e', 'Name': 'trusting_hugle'
            },
            {
                'Image': '95270569baf6', 'Container_Id': '0a6692ebea53', 'Name': 'dreamy_roentgen'
            }
        ]

        self.assertEquals(result, expected_result)

    def test_general_parse_with_docker_get_valid(self):

        data = docker_inspect_string

        result = self.ssh.general_parse(
            text=data, fsm="./conf/docker_get.fsm")

        expected_result = [{
            'Image': '95270569baf65db9449b7dff671b8f6c14af0c7c66cc220a1189c6915d33cb62',
            'Id': 'a1338284534e3e352bebdfbe7110a067c98e51575a8329482a5bba498785817f',
            'Name': 'trusting_hugle'
        }]

        self.assertEquals(result, expected_result)

    def test_general_parse_with_docker_post_valid(self):

        data = "734c0923794d3c0c2c18374ccd320a01db1ec7ae31b8703c9992186d4609207d"

        result = self.ssh.general_parse(
            text=data, fsm="./conf/docker_post.fsm")

        expected_result = [{
            'Container_Id': '734c0923794d3c0c2c18374ccd320a01db1ec7ae31b8703c9992186d4609207d'
        }]

        self.assertEquals(result, expected_result)

    def test_general_parse_with_docker_delete_valid(self):

        data = "734c0923794d3c0c2c18374ccd320a01db1ec7ae31b8703c9992186d4609207d"

        result = self.ssh.general_parse(
            text=data, fsm="./conf/docker_delete.fsm")

        expected_result = [{
            'Container': '734c0923794d3c0c2c18374ccd320a01db1ec7ae31b8703c9992186d4609207d'
        }]

        self.assertEquals(result, expected_result)

    def test_general_parse_invalid_no_match(self):

        data = "Invalid string"
        result = self.ssh.general_parse(
            text=data, fsm="./conf/sysconfig_get.fsm")
        self.assertEquals(result, "Not found: No data could be retrieved")

    def test_general_parse_invalid_no_fsm(self):

        data = ("Linux CLPSTPDFC115 3.19.0-25-generic #26~14.04.1-Ubuntu SMP "
                + "Fri Jul 24 21:16:20 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux")
        result = self.ssh.general_parse(
            text=data, fsm="invalid.fsm")

        self.assertEquals(
            result, "Internal server error: Error occured either while opening fsm file or while creating parser")

    def test_handle_quotes_valid(self):

        data = [u'docker', u'ps', u'-a', u'--format',
                u"'{{.ID}}", u'{{.Image}}', u"{{.Names}}'"]

        result = self.ssh.handle_quotes(data)
        expected_result = [u'docker', u'ps', u'-a',
                           u'--format', u"'{{.ID}} {{.Image}} {{.Names}}'"]

        self.assertEquals(result, expected_result)

    def test_handle_quotes_open_quotes(self):

        data = [u'docker', u'ps', u'-a', u'--format',
                u"'{{.ID}}", u'{{.Image}}', u"{{.Names}}"]

        with self.assertRaises(Exception) as cm:
            result = self.ssh.handle_quotes(data)

        self.assertEquals(cm.exception.message,
                          "Unclosed quote in shell command")

    def test_send_sysconfig_get_valid(self):

        command_output = ("Linux CLPSTPDFC115 3.19.0-25-generic #26~14.04.1-Ubuntu SMP Fri Jul 24 21:16:20 UTC 2015 "
                          + "x86_64 x86_64 x86_64 GNU/Linux")

        shell_result = ExecutionResult(
            return_code=0, stderr_output="", output=command_output)

        self.ssh.shell.run = MagicMock(return_value=shell_result)

        result = self.ssh.send("sysconfig", "get")

        expected_result = {
            'credentials': 'username:password', 'version': 1,
            'properties': [{
                'Name': 'CLPSTPDFC115', 'Description': '64 bit system running 3.19.0-25-generic'
            }]
        }

        self.assertEquals(result, expected_result)

    def test_send_docker_get_valid(self):

        command_output = "'a1338284534e ubuntu trusting_hugle'\n'0a6692ebea53 95270569baf6 dreamy_roentgen'"

        shell_result = ExecutionResult(
            return_code=0, stderr_output="", output=docker_inspect_string)

        self.ssh.shell.run = MagicMock(return_value=shell_result)

        result = self.ssh.send("docker", "get", "a1338284534e")

        expected_result = {
            'credentials': 'username:password', 'version': 1,
            'properties': [{
                'Image': '95270569baf65db9449b7dff671b8f6c14af0c7c66cc220a1189c6915d33cb62',
                'Id': 'a1338284534e3e352bebdfbe7110a067c98e51575a8329482a5bba498785817f',
                'Name': 'trusting_hugle'
            }]
        }

        self.assertEquals(result, expected_result)

    def test_send_docker_list_valid(self):

        command_output = "'a1338284534e ubuntu trusting_hugle'\n'0a6692ebea53 95270569baf6 dreamy_roentgen'"

        shell_result = ExecutionResult(
            return_code=0, stderr_output="", output=command_output)

        self.ssh.shell.run = MagicMock(return_value=shell_result)

        result = self.ssh.send("docker", "list")

        expected_result = {
            'credentials': 'username:password', 'version': 1,
            'properties': [
                {
                    'Image': 'ubuntu', 'Container_Id': 'a1338284534e', 'Name': 'trusting_hugle'
                },
                {
                    'Image': '95270569baf6', 'Container_Id': '0a6692ebea53', 'Name': 'dreamy_roentgen'
                }
            ]
        }

        self.assertEquals(result, expected_result)

    def test_send_docker_post_valid(self):

        command_output = "734c0923794d3c0c2c18374ccd320a01db1ec7ae31b8703c9992186d4609207d"

        shell_result = ExecutionResult(
            return_code=0, stderr_output="", output=command_output)

        self.ssh.shell.run = MagicMock(return_value=shell_result)

        result = self.ssh.send(
            "docker", "post", "--name=ContainerX", "24d48ae3a433")

        expected_result = {
            'credentials': 'username:password', 'version': 1,
            'properties': [{
                'Container_Id': '734c0923794d3c0c2c18374ccd320a01db1ec7ae31b8703c9992186d4609207d'
            }]
        }

        self.assertEquals(result, expected_result)

    def test_send_docker_delete_valid(self):

        command_output = "734c0923794d3c0c2c18374ccd320a01db1ec7ae31b8703c9992186d4609207d"

        shell_result = ExecutionResult(
            return_code=0, stderr_output="", output=command_output)

        self.ssh.shell.run = MagicMock(return_value=shell_result)

        result = self.ssh.send("docker", "delete", "734c0923794d")

        expected_result = {
            'credentials': 'username:password', 'version': 1,
            'properties': [{
                'Container': '734c0923794d3c0c2c18374ccd320a01db1ec7ae31b8703c9992186d4609207d'
            }]
        }

        self.assertEquals(result, expected_result)

    def test_send_invalid_running_command_throws_exception_internal_server_error(self):

        self.ssh.shell.run = MagicMock(
            side_effect=Exception("Something went wrong"))
        result = self.ssh.send("sysconfig", "get")
        self.assertEquals(
            result, "Internal server error: Something went wrong")

    def test_send_invalid_running_command_throws_exception_authorization_error(self):

        self.ssh.shell.run = MagicMock(
            side_effect=Exception("Authorization failed"))
        result = self.ssh.send("sysconfig", "get")
        self.assertEquals(result, "Authorization error: Authorization failed")

    def test_send_invalid_running_command_throws_exception_authentication_error(self):

        self.ssh.shell.run = MagicMock(
            side_effect=Exception("Authentication failed"))
        result = self.ssh.send("sysconfig", "get")
        self.assertEquals(
            result, "Authentication error: Authentication failed")

    def test_get_sysconfig_valid(self):

        command_output = ("Linux CLPSTPDFC115 3.19.0-25-generic #26~14.04.1-Ubuntu SMP Fri Jul 24 21:16:20 UTC 2015 "
                          + "x86_64 x86_64 x86_64 GNU/Linux")

        shell_result = ExecutionResult(
            return_code=0, stderr_output="", output=command_output)

        self.ssh.shell.run = MagicMock(return_value=shell_result)
        result = self.ssh.get("sysconfig")

        expected_result = {
            'credentials': 'username:password',
            'version': 1,
            'properties': [{
                'Name': 'CLPSTPDFC115',
                'Description': '64 bit system running 3.19.0-25-generic'
            }]
        }

        self.assertEquals(result, expected_result)

    def test_get_sysconfig_invalid(self):

        self.ssh.shell.run = MagicMock(
            side_effect=Exception("Something went wrong"))

        result = self.ssh.get("sysconfig")

        self.assertEquals(
            result, "Internal server error: Something went wrong")

    def test_get_docker_valid(self):

        command_output = "'a1338284534e ubuntu trusting_hugle'\n'0a6692ebea53 95270569baf6 dreamy_roentgen'"

        shell_result = ExecutionResult(
            return_code=0, stderr_output="", output=docker_inspect_string)

        self.ssh.shell.run = MagicMock(return_value=shell_result)

        result = self.ssh.get("docker", "a1338284534e")

        expected_result = {
            'credentials': 'username:password', 'version': 1,
            'properties': [{
                'Image': '95270569baf65db9449b7dff671b8f6c14af0c7c66cc220a1189c6915d33cb62',
                'Id': 'a1338284534e3e352bebdfbe7110a067c98e51575a8329482a5bba498785817f',
                'Name': 'trusting_hugle'
            }]
        }

        self.assertEquals(result, expected_result)

    def test_get_docker_invalid(self):

        self.ssh.shell.run = MagicMock(
            side_effect=Exception("Something went wrong"))

        result = self.ssh.get("docker", "a1338284534e")

        self.assertEquals(
            result, "Internal server error: Something went wrong")

    def test_list_docker_valid(self):

        command_output = "'a1338284534e ubuntu trusting_hugle'\n'0a6692ebea53 95270569baf6 dreamy_roentgen'"

        shell_result = ExecutionResult(
            return_code=0, stderr_output="", output=command_output)

        self.ssh.shell.run = MagicMock(return_value=shell_result)

        result = self.ssh.list("docker")

        expected_result = {
            'credentials': 'username:password', 'version': 1,
            'properties': [
                {
                    'Image': 'ubuntu', 'Container_Id': 'a1338284534e', 'Name': 'trusting_hugle'
                },
                {
                    'Image': '95270569baf6', 'Container_Id': '0a6692ebea53', 'Name': 'dreamy_roentgen'
                }
            ]
        }

        self.assertEquals(result, expected_result)

    def test_list_docker_invalid(self):

        self.ssh.shell.run = MagicMock(
            side_effect=Exception("Something went wrong"))

        result = self.ssh.list("docker")

        self.assertEquals(
            result, "Internal server error: Something went wrong")

    def test_post_docker_valid(self):

        command_output = "734c0923794d3c0c2c18374ccd320a01db1ec7ae31b8703c9992186d4609207d"

        shell_result = ExecutionResult(
            return_code=0, stderr_output="", output=command_output)

        self.ssh.shell.run = MagicMock(return_value=shell_result)

        result = self.ssh.post("docker", "--name=ContainerX", "24d48ae3a433")

        expected_result = {
            'credentials': 'username:password', 'version': 1,
            'properties': [{
                'Container_Id': '734c0923794d3c0c2c18374ccd320a01db1ec7ae31b8703c9992186d4609207d'
            }]
        }

        self.assertEquals(result, expected_result)

    def test_post_invalid(self):

        self.ssh.shell.run = MagicMock(
            side_effect=Exception("Something went wrong"))

        result = self.ssh.post("docker", "--name=ContainerX", "24d48ae3a433")

        self.assertEquals(
            result, "Internal server error: Something went wrong")

    def test_delete_docker_valid(self):

        command_output = "734c0923794d3c0c2c18374ccd320a01db1ec7ae31b8703c9992186d4609207d"

        shell_result = ExecutionResult(
            return_code=0, stderr_output="", output=command_output)

        self.ssh.shell.run = MagicMock(return_value=shell_result)

        result = self.ssh.delete("docker", "734c0923794d")

        expected_result = {
            'credentials': 'username:password', 'version': 1,
            'properties': [{
                'Container': '734c0923794d3c0c2c18374ccd320a01db1ec7ae31b8703c9992186d4609207d'
            }]
        }

        self.assertEquals(result, expected_result)

    def test_delete_docker_invalid(self):

        self.ssh.shell.run = MagicMock(
            side_effect=Exception("Something went wrong"))

        result = self.ssh.delete("docker", "734c0923794d")

        self.assertEquals(
            result, "Internal server error: Something went wrong")

    def test_put_not_allowed(self):

        with self.assertRaises(NotImplementedError) as cm:
            self.ssh.put("docker", "734c0923794d")

        self.assertEquals(cm.exception.message, "Method not allowed: SSH currently supports GET, POST, DELETE and LIST.")


def main():
    unittest.main()


if __name__ == '__main__':
    main()
