
import textfsm
import spur


class SSH(object):

    def __init__(self, host, user, pas):
        """ Initialize SSH object with host, username and pasword """
        self.host = host
        self.user = user
        self.pas = pas

    def parse(self, text, template, error):
        """ Parse text according to template and then convert to json """

        if error:
            return {"error": text, "response": None}
        response = {"error": None}

        with open(template) as f:
            parser = textfsm.TextFSM(f)

        lists = parser.ParseText(text)

        parsed = []
        for i in xrange(len(lists)):
            elem = {}
            for j in xrange(len(parser.header)):
                elem[parser.header[j]] = lists[i][j]
            parsed.append(elem)
        response["response"] = parsed

        return response

    def get(self, command, template):
        """ Run given command on remote host and returns results. Calls parse function with result and template """

        command = command.split()
        shell = spur.SshShell(hostname=self.host, username=self.user, password=self.pas,
                              missing_host_key=spur.ssh.MissingHostKey.accept, connect_timeout=5)
        try:
            with shell:
                result = shell.run(command)
        except Exception, e:
            response = e.message.replace("\n", " ")
            error = True
        else:
            response = result.output
            error = False

        return self.parse(response, template, error)


def main():

    from sys import argv
    host, user, pas, command, template = argv[1:]

    ssh = SSH(host, user, pas)
    print ssh.get(command, template)


if __name__ == '__main__':
    main()
