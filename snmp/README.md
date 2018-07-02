====
snmp
====


The file snmp.py  contains code implementing snmp get, set and get_next commands.

It is hardcoded to send requests to IP 127.0.0.1 at port 1678. 
    
This device is simulated via snmp simulator to facilitate testing of the set command.

You can find more information about the simulator here:

```
http://www.ireasoning.com/snmpsimulator.shtml
```
Please note that the simulator is an evaluation version and will expire after a 30 day time period.

It can only be run for 30 minutes at a time.

To run the snmp simulator, execute the following command:

```
<your_directory>/ireasoning/simulator/bin/./runUI.sh
```
Once simulator is running, create a project that  will simulate an snmp device running on IP 127.0.0.1 on port 1678.

Now snmp.py can be run via the command line by passing a JSON file contaning therequest as an argument as follows:

```
python snmp.py <JSON file>
```

Here `` <JSON file> `` is a JSON file.
JSON requests are contained in the subdirectory 'requests'.

For example, to run a file containg a sample get request, execute the following command:

```
python snmp.py requests/get.json
```

The result is returned as JSON.

The file snmp_trap.py contains code implementing a trap receiver that is hardcoded to listen on IP 127.0.0.1 at port 10000.

The program is executed as follows:

```
python snmp_trap.py
```

To send traps to this receiver, the mib browser has to be utilized. 

More information about mib browser can be found here:
```
http://www.ireasoning.com/mibbrowser.shtml
```
To run the mib browser, execute the following command:

```
<your_directory>/ireasoning/mibbrowser/browser.sh
```

Under the tools menu, run the trap sender. Use it to send a trap to IP 127.0.0.1 at port 10000.

This trap will be received by the python program and output will be displayed as JSON.
