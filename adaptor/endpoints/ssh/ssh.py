import textfsm
import spur
import json
import sys
sys.path.insert(0, "/home/username/programs")
from adaptor.protocol_handler import Protocol_Handler


CONF = "./conf/ssh.conf"


sys_config_mapping = {
    "Name": {},
    "Description": {
        "x86_64": "64 bit system running",
        "i686": "32 bit system running"
    },


}i


def sysconfig_get_parse(data):  # Data is a dictionary
    """ Parsing specific to sysconfig get operation"""

    parsed = {}
    data = data[0]  # For sysconfig, we know list has one element

    parsed['Name'] = sys_config_mapping["Name"].get(data['Name'], data['Name'])
    parsed['Description'] = sys_config_mapping["Description"].get(data['Architecture'], "Unknown processor running") + data["Kernel"]

    # Put dictionary in list to be consistent with other data sent to upper layer
    parsed = [parsed]

    return parsed


# Dictionary mapping operation names to corresponding parse functions
specific_parsers = {
    "sysconfig_get": sysconfig_get_parse
}


class SSH(Protocol_Handler):

    def __init__(self, endpoint):
        """ Initialize SSH object with various attributes.
            Create shell object with some of these attributes and attach it to SSH object.
        """
        self.ip = endpoint.ip
        self.port = endpoint.port if endpoint.port else 22
        self.credentials = endpoint.cred
        self.user, self.password = self.credentials.split(":")
        self.version = int(endpoint.version)
        if self.version != 1:
            raise Exception("Bad request: Version not supported")

        self.shell = spur.SshShell(hostname=self.ip, port=self.port, username=self.user, password=self.password,
                                   missing_host_key=spur.ssh.MissingHostKey.accept, connect_timeout=5)

    def specific_parse(self, response, parser_name):
        """ Do feature and operation specific parsing if specific parser is available """

        parser = specific_parsers.get(parser_name, None)
        return parser(response) if parser else response

    def general_parse(self, text, fsm):
        """ Parse text according to fsm and convert to list of dictionaries
            Return error as string if something goes wrong
        """
        try:
            with open(fsm) as f:
                parser = textfsm.TextFSM(f)
        except:
            return ("Internal server error: "
                    + "Error occured either while opening fsm file or while creating parser")

        lists = parser.ParseText(text)

        if not len(lists):
            return "Not found: No data could be retrieved"

        parsed = []
        for i in xrange(len(lists)):
            elem = {}
            for j in xrange(len(parser.header)):
                elem[parser.header[j]] = lists[i][j]
            parsed.append(elem)

        return parsed

    def handle_quotes(self, command):
        """ Combine elements from starting quote to ending quote in command list """

        double_quoted = False
        single_quoted = False
        parsed_command = []
        new_elem = ""

        for elem in command:

            if single_quoted or double_quoted:
                new_elem += " " + elem
                if elem.endswith('"'):
                    double_quoted = False
                    parsed_command.append(new_elem)
                    new_elem = ""

                elif elem.endswith("'"):
                    single_quoted = False
                    parsed_command.append(new_elem)
                    new_elem = ""

            elif elem.startswith("'") or elem.startswith("'"):
                new_elem += elem
                if elem.startswith('"'):
                    double_quoted = True
                elif elem.startswith("'"):
                    single_quoted = True

            else:
                parsed_command.append(elem)

        if single_quoted or double_quoted:
            raise Exception, "Unclosed quote in shell command"
        else:
            return parsed_command

    def send(self, feature_name, operation, *args):
        """ Get command and fsm from conf file
            Run command on device and get result
            Call parse functions on result and return
        """

        try:
            with open(CONF) as f:
                conf = json.load(f)[feature_name]
            fsm = conf[operation]["fsm"]
            command = conf[operation]["command"].split()
            command = self.handle_quotes(command)
            command += list(args)

            with self.shell:
                result = self.shell.run(command)

        except KeyError:
            return "Not found: Feature not found in conf file"
        except IOError:
            return "Internal server error: There was an error opening conf file"
        except Exception, e:
            error = e.message.encode("utf-8")  # Convert unicode to string
            error = error.replace("\n", " ")

            if "authenticat" in error.lower():
                error = "Authentication error: " + error
            elif "authoriz" in error.lower():
                error = "Authorization error: " + error
            else:
                error = "Internal server error: " + error
            return error

        result = result.output
        result = self.general_parse(result, fsm)

        if type(result) is str:  # String indicates error
            return result

        parser_name = feature_name + "_" + operation
        result = self.specific_parse(result, parser_name)

        # Return response
        return {"version": self.version, "credentials": self.credentials, "properties": result}

    def get(self, feature_name, *args):
        return self.send(feature_name, "get", *args)

    def list(self, feature_name, *args):
        return self.send(feature_name, "list", *args)

    def post(self, feature_name, *args):
        return self.send(feature_name, "post", *args)

    def delete(self, feature_name, *args):
        return self.send(feature_name, "delete", *args)

    def put(self, feature_name, *args):
        raise NotImplementedError(
            "Method not allowed: SSH currently supports GET, POST, DELETE and LIST.")
