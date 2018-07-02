===
ssh
===

The file ssh.py in this directory connects to a remote host, runs a given command on that system and returns a result parsed according to a template and then converted to JSON.

Templates are contained in the subdirectory 'templates'.


Run with the following command:
```
python ssh.py <ip> <username> <password> <command> <<template>
```

Example command:

```
python ssh.py 172.23.106.201 username password "ls -la" templates/ls_template
```
