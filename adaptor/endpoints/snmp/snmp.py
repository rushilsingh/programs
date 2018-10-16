from pysnmp.proto.rfc1902 import *
from pysnmp.proto.rfc1902 import ObjectName
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto.rfc1905 import NoSuchObject, EndOfMibView
from pysnmp.proto import api
from pysnmp.carrier.twisted.dgram import udp
from twisted.internet import defer
from time import time
from sys import argv
import json
from twisted.internet import reactor
import sys
sys.path.insert(0, "/home/username/programs")
from adaptor.protocol_handler import Protocol_Handler


types = {
    "OctetString": OctetString,
    "Integer": Integer,
    "Integer32": Integer32,
    "TimeTicks": TimeTicks,
    "Counter32": Counter32,
    "Counter64": Counter64,
    "Gauge32": Gauge32,
    "Bits": Bits,
    "Opaque": Opaque,
    "IpAddress": IpAddress,
    "ObjectIdentifer": ObjectIdentifier,
    "ObjectName": ObjectName,
    "Unsigned32": Unsigned32
}
        if self.version == 1:
            self.apiVersion = api.protoModules[api.protoVersion1]
        elif self.version == 2:
            self.apiVersion = api.protoModules[api.protoVersion2c]


version_mapping = {1:api.protoModules[api.protoVersion1] , 2:api.protoModules[api.protoVersion2c}

GET = 1
GET_NEXT = 2
CONF = "./conf/snmp.conf"


def extract_values(data):
    """ Extract values from ASN.1 objects """
    extracted = []
    for (oid, value) in data:
        oid = ".".join(str(i) for i in oid.asTuple())

        if isinstance(value, OctetString):
            value = value.asOctets()
        elif isinstance(
                value, (Integer, Integer32, Unsigned32, TimeTicks, Counter32, Counter64, Gauge32)):
            value = int(value)
        else:
            value = str(value)
        extracted.append((oid, value))
    return extracted


def to_json(data):
    """ Convert list of tuples to json """

    result = {}
    for (oid, val) in data:
        result[oid] = val
    return result


def to_names(pairs, feature_name):
    """ Change dictionary with oid, value pairs to dictionary with name, value pairs based on feature name """

    with open(CONF) as f:
        mappings = json.load(f)[feature_name]

    result = {}
    for oid, value in pairs.items():
        for name in mappings:
            target = mappings[name][0]

            if oid == target:
                result[name] = value

            elif oid.startswith(target):
                last = oid.split(target)[-1]
                result[name + last] = value

    return result


def args_from_feature(feature_name, operation):
    """ Get arguments for SNMP request from snmp.conf file """

    with open(CONF) as f:
        mappings = json.load(f)[feature_name]

    if operation == GET or operation == GET_NEXT:
        oids = [pair[0] for pair in mappings.values()]

    # if operation == SET then we have to build ASN.1 objects
    # and then make a list of tuples in this format: [(oid1, object1), (oid2, object2), ...]

    return oids


def check_for_errors(arguments, operation):
    """ Check if arguments are valid for given operation
        Raise Exception if any argument is invalid, else return
    """

    if type(arguments[0]) is tuple:
        arguments = [arg[0] for arg in arguments]

    # All valid OIDs must have this prefix
    valid = [arg.startswith("1.3.6.1.2.1") for arg in arguments]
    valid = all(valid)
    if not valid:
        raise Exception("Bad request: Invalid OID")
    else:
        scalar = [arg.endswith("0") for arg in arguments]
        scalar = any(scalar)

        if operation == GET and not scalar:
            raise Exception(
                "Method not allowed: Tabular not supported for get")
        elif operation == GET_NEXT and scalar:
            raise Exception(
                "Method not allowed: Scalar not supported for get_next")
        else:
            return


class CustomUDPTransport(udp.UdpTransport):

    def __init__(self, *args, **kwargs):
        self.dObj = None
        super(CustomUDPTransport, self).__init__(*args, **kwargs)


class SNMP(Protocol_Handler):

    def __init__(self, endpoint):

        self.version = int(endpoint.version)
        self.credentials = endpoint.cred

        self.readCommunity, self.writeCommunity = self.credentials.split(":")

        endpoint.port = endpoint.port if endpoint.port else 161
        self.target = (endpoint.ip, endpoint.port)

        self.apiVersion = version_mapping.get(self.version)
        if not self.apiVersion:
            raise Exception, "Bad request: Version not supported"

        self.transportObj = CustomUDPTransport()
        self.transportObj.openClientMode()
        self.transportObj.registerCbFun(self._receiveCb)

    def _buildMsg(self, community,  oids, command):
        """ Build Request Message """

        if command == GET:
            reqPDU = self.apiVersion.GetRequestPDU()
            binds = [(oid, self.apiVersion.Null('')) for oid in oids]
        elif command == GET_NEXT:
            reqPDU = self.apiVersion.GetNextRequestPDU()
            binds = [(oid, self.apiVersion.Null('')) for oid in oids]
        elif command == SET:
            reqPDU = self.apiVersion.SetRequestPDU()
            binds = oids
        else:
            raise Exception, "Bad request: Command not recognized"

        self.apiVersion.apiPDU.setDefaults(reqPDU)
        self.apiVersion.apiPDU.setVarBinds(reqPDU, binds)

        reqMsg = self.apiVersion.Message()
        self.apiVersion.apiMessage.setDefaults(reqMsg)
        self.apiVersion.apiMessage.setCommunity(reqMsg, community)
        self.apiVersion.apiMessage.setPDU(reqMsg, reqPDU)
        reqMsg = encoder.encode(reqMsg)

        # Storing in self.reqMsg because access to request message is needed in _receiveCb
        # to match requestID of request PDU and response PDU
        self.reqMsg = reqMsg
        return reqMsg

    def _timeoutCb(self):
        if self.transportObj.dObj:
            d, self.transportObj.dObj = self.transportObj.dObj, None
            d.errback(Exception("Timeout: No response received"))
        return

    def _receiveCb(self, transportObj, address, wholeMsg):
        """ Receive response PDU and callback deferred with extracted variable bindings """

        err = None
        data = []

        # Decode request message from self.reqMsg
        reqMsg, _ = decoder.decode(
            self.reqMsg, asn1Spec=self.apiVersion.Message())
        # Extract request PDU
        reqPDU = self.apiVersion.apiMessage.getPDU(reqMsg)

        while wholeMsg:
            rspMsg, wholeMsg = decoder.decode(
                wholeMsg, asn1Spec=self.apiVersion.Message())
            rspPDU = self.apiVersion.apiMessage.getPDU(rspMsg)

            # Match response to request
            if self.apiVersion.apiPDU.getRequestID(reqPDU) == self.apiVersion.apiPDU.getRequestID(rspPDU):
                # Remove deferred from transport so no timeout
                d, transportObj.dObj = transportObj.dObj, None
                # Check for SNMP errors reported
                errorStatus = self.apiVersion.apiPDU.getErrorStatus(rspPDU)
                if errorStatus:
                    err = Exception(errorStatus.prettyPrint())

                else:
                    for oid, val in self.apiVersion.apiPDU.getVarBinds(rspPDU):
                        if type(val) is NoSuchObject:
                            err = Exception("Not found: noSuchName")
                        elif type(val) is EndOfMibView:
                            err = Exception("Not found: EndOfMibView")
                        else:
                            data.append((oid, val))
        if err:
            d.errback(err)
        else:
            d.callback(data)

        return wholeMsg

    @defer.inlineCallbacks
    def send(self, msg):
        """ Send Request Message. Add callbacks to response and return deferred result """

        d = defer.Deferred()
        d.addCallbacks(extract_values, lambda x: x.getErrorMessage())
        self.transportObj.dObj = d
        try:
            self.transportObj.sendMessage(msg, self.target)
        except:
            defer.returnValue(
                "Bad request: Could not send message to target device")
        else:
            reactor.callLater(5, self._timeoutCb)
            res = yield d
            defer.returnValue(res)

    @defer.inlineCallbacks
    def get(self, feature_name, *args):
        """ Get values from snmp device for provided feature"""

        try:
            oids = args_from_feature(feature_name, GET)
            check_for_errors(oids, GET)
        except IOError:
            response = "Internal server error: There was an error opening conf file"
        except KeyError:
            response = "Not found: Feature not found in conf file"
        except Exception, e:
            response = e.message
        else:
            msg = self._buildMsg(self.readCommunity, oids, GET)
            data = yield self.send(msg)

            if type(data) is str:  # String indicates error message
                response = data
            else:
                # Put into list for consistency with other data sent to APIHandler layer
                data = [to_names(to_json(data), feature_name)]

                # Construct response
                response = {}
                response['properties'] = data
                response['version'] = self.version
                response['credentials'] = self.credentials

        self.transportObj.closeTransport()
        defer.returnValue(response)

    def post(self, feature_name, *args):
        raise NotImplementedError(
            "Method not allowed: SNMP currently supports only GET")

    def put(self, feature_name, *args):
        raise NotImplementedError(
            "Method not allowed: SNMP currently supports only GET")

    def list(self, feature_name, *args):
        raise NotImplementedError(
            "Method not allowed: SNMP currently supports only GET")

    def delete(self, feature_name, *args):
        raise NotImplementedError(
            "Method not allowed: SNMP currently supports only GET")
