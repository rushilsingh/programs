from pyasn1.type.univ import *
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto.rfc1905 import NoSuchObject, EndOfMibView
from pysnmp.proto import api
from pysnmp.carrier.twisted.dgram import udp
from twisted.internet import defer
from time import time
from sys import argv
import json

IP, PORT = '127.0.0.1', 10000

trap_mappings = {
    "1.3.6.1.6.3.1.1.5.1": 'coldStart',
    "1.3.6.1.6.3.1.1.5.2": 'warmStart',
    "1.3.6.1.6.3.1.1.5.3": 'linkDown',
    "1.3.6.1.6.3.1.1.5.4": 'linkUp',
    "1.3.6.1.6.3.1.1.5.5": "authenticationFailure",
    "1.3.6.1.6.3.1.1.5.6": "egpNeighborLoss",
}


def extract(data):
    """ Extract values from ASN.1 objects """

    extracted = []
    for (oid, value) in data:
        oid = ".".join(str(i) for i in oid.asTuple())

        if isinstance(value, OctetString):
            value = value.asOctets()
        elif isinstance(value, Integer):
            value = int(value)
        else:
            value = str(value)
        extracted.append((oid, value))
    return extracted


def parse(data):
    """ Populate response based on data fields """

    parsed = {}
    parsed["Source"], parsed["Uptime"], parsed["Additional"] = data["Source"], data["Uptime"], data["Varbinds"]

    if data["Generic"] == "enterpriseSpecific":
        parsed["Severity"] = "Unknown"
        parsed["Description"] = "This is an enterprise specific trap"
        if data["Version"] == 1:
            parsed["TrapType"] = data["Generic"] + "." + data["Specific"]
            parsed["Additional"]["Enterprise OID"] = data["Enterprise OID"] + \
                ".0." + data["Specific"]
        else:
            parsed["TrapType"] = data["Generic"]
            parsed["Additional"]["Enterprise OID"] = data["Enterprise OID"]
    else:
        parsed["TrapType"] = data["Generic"]

        if parsed["TrapType"] == "coldStart":
            parsed["Severity"] = 4
            parsed["Description"] = "Sending entity reinitialized with alterations"

        elif parsed["TrapType"] == "warmStart":
            parsed["Severity"] = 4
            parsed["Description"] = "Sending entity reinitialized without alterations"

        elif parsed["TrapType"] == "linkDown":
            parsed["Severity"] = 5
            parsed["Description"] = "There was a failure in a communication link"

        elif parsed["TrapType"] == "linkUp":
            parsed["Severity"] = 2
            parsed["Description"] = "A communication link has come up"

        elif parsed["TrapType"] == "authenticationFailure":
            parsed["Severity"] = 5
            parsed["Description"] = " Sending entity received message with improper authentication"

        elif parsed["TrapType"] == "egpNeighborLoss":
            parsed["Severity"] = 3
            parsed["Description"] = "An EGP Neighbour is no longer a peer"
    return parsed


def parse_v2(data):
    """ Process v2 trap into format that can be fed into parse function """

    parsed = {}
    parsed["Version"] = 2
    parsed["Uptime"] = data[0][1]
    trap_oid = data[1][1]
    if trap_oid in trap_mappings:
        parsed["Generic"] = trap_mappings[trap_oid]
    else:
        parsed["Generic"] = "enterpriseSpecific"
        parsed["Enterprise OID"] = trap_oid

    varbinds = data[2:]
    parsed["Varbinds"] = {}
    for oid, val in varbinds:
        parsed["Varbinds"][oid] = val
    return parsed


class SNMP(object):

    def __init__(self, ip, port):

        transport = udp.UdpTransport()
        transport.openServerMode((ip, port))
        transport.registerCbFun(self._receiveCb)

    def _receiveCb(self, transportObj, address, wholeMsg):

        data = {}
        while wholeMsg:
            msgVersion = int(api.decodeMessageVersion(wholeMsg))
            apiVersion = api.protoModules[msgVersion]
            reqMsg, wholeMsg = decoder.decode(
                wholeMsg, asn1Spec=apiVersion.Message())

            reqPDU = apiVersion.apiMessage.getPDU(reqMsg)
            if reqPDU.isSameTypeWith(apiVersion.TrapPDU()):
                if msgVersion == api.protoVersion1:

                    data["Enterprise OID"] = apiVersion.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()
                    data["Source"] = apiVersion.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()
                    data["Generic"] = apiVersion.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint().replace("'", "")
                    data["Specific"] = apiVersion.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()
                    data["Uptime"] = apiVersion.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()
                    varBinds = apiVersion.apiTrapPDU.getVarBinds(reqPDU)
                    data["Varbinds"] = {}
                    for oid, val in varBinds:
                        data["Varbinds"][oid.prettyPrint()] = val.prettyPrint()
                    data["Version"] = 1
                else:
                    varBinds = apiVersion.apiPDU.getVarBinds(reqPDU)
                    data = parse_v2(extract(varBinds))
                    data["Source"], _ = address
                    data["Version"] = 2

        print parse(data)
        return wholeMsg


def main():

    snmp = SNMP(IP, PORT)
    from twisted.internet import reactor
    reactor.run()


if __name__ == '__main__':
    main()
