from pyasn1.type.univ import *
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto.rfc1905 import NoSuchObject, EndOfMibView
from pysnmp.proto import api
from pysnmp.carrier.twisted.dgram import udp
from twisted.internet import defer
from time import time
from sys import argv
import json
from twisted.internet import reactor

GET = 1
GET_NEXT = 2
SET = 3
IP, PORT = '127.0.0.1', 1678

mappings = {
    "sysDescr": ('1.3.6.1.2.1.1.1.0', OctetString),
    "sysContact": ('1.3.6.1.2.1.1.4.0', OctetString),
    "sysUpTime": ('1.3.6.1.2.1.1.3.0', Integer),
    "ifNumber": ('1.3.6.1.2.1.2.1.0', Integer),
    "sysLocation": ('1.3.6.1.2.1.1.6.0', OctetString),
    "sysName": ('1.3.6.1.2.1.1.5.0', OctetString),
    "ifIndex": ('1.3.6.1.2.1.2.2.1.1', Integer),
    "ifDescr": ('1.3.6.1.2.1.2.2.1.2', OctetString),
    "ifDescr.4":('1.3.6.1.2.1.2.2.1.2.4', OctetString),
    "invalid": ('1.3.6.1.2.1.99.0', OctetString),
    "invalid_tabular": ('1.3.6.1.2.1.44', OctetString)
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


def to_json(data):
    """ Convert list of tuples to json """

    result = {}
    for (oid, val) in data:
        result[oid] = val
    return result


def to_names(pairs):
    """ Change oid, value pairs to name, value pairs """

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


def response(version, community, op, res):
    """ Construct json response from fields """

    if type(res) is str:
        error = res
        varbinds = None
    else:
        error = None
        varbinds = res
    response = {"version": version, "community": community,
                "operation": op, "error": error, "vars": varbinds}
    return response


def from_file():
    """ Reads json data from file and loads it into a dictionary """

    fname = argv[1]
    with open(fname) as f:
        result = json.load(f)
    return result


def get_arguments(variables):
    """ Gets variable bindings from file and parses them
        into arguments for various operations """

    if type(variables) is list:
        res = [mappings[name][0] for name in variables]
    elif type(variables) is dict:
        res = []
        for name, value in variables.items():
            oid = mappings[name][0]
            wrapped = mappings[name][1](value)
            res.append((oid, wrapped))
    else:
        raise Exception, "Variables in unsupported format"
    return res


def check(arguments, op):
    """ Check if arguments are valid for given operation
        Raise Exception if present, else return """

    if type(arguments[0]) is tuple:
        arguments = [arg[0] for arg in arguments]

    valid = [arg.startswith("1.3.6.1.2.1") for arg in arguments]
    valid = all(valid)
    if not valid:
        raise Exception("Invalid oid")
    else:
        scalar = [arg.endswith("0") for arg in arguments]
        scalar = any(scalar)

        if op == "get" and not scalar:
            raise Exception("tabular not supported for get")
        elif op == "get_next" and scalar:
            raise Exception("scalar not supported for get_next")
        else:
            return


class CustomUDPTransport(udp.UdpTransport):

    def __init__(self, *args, **kwargs):
        self.dObj = None
        super(CustomUDPTransport, self).__init__(*args, **kwargs)


class SNMP(object):

    def __init__(self, version, community, ip, port):

        if version == 1:
            self.version = 1
            self.apiVersion = api.protoModules[api.protoVersion1]
        elif version == 2:
            self.version = 2
            self.apiVersion = api.protoModules[api.protoVersion2c]
        else:
            raise Exception, "Version not supported"

        self.community = community
        self.target = (ip, port)

        self.transportObj = CustomUDPTransport()
        self.transportObj.openClientMode()
        self.transportObj.registerCbFun(self._receiveCb)

    def _buildMsg(self, oids, command):
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
            raise Exception, "Command not supported"
        self.apiVersion.apiPDU.setDefaults(reqPDU)
        self.apiVersion.apiPDU.setVarBinds(reqPDU, binds)

        reqMsg = self.apiVersion.Message()
        self.apiVersion.apiMessage.setDefaults(reqMsg)
        self.apiVersion.apiMessage.setCommunity(reqMsg, self.community)
        self.apiVersion.apiMessage.setPDU(reqMsg, reqPDU)
        reqMsg = encoder.encode(reqMsg)

        # Storing in self.reqMsg because access to request message is needed in _receiveCb
        # to match requestID of request PDU and response PDU
        self.reqMsg = reqMsg
        return reqMsg

    def _timeoutCb(self):
        if self.transportObj.dObj:
            d, self.transportObj.dObj = self.transportObj.dObj, None
            d.errback(Exception("Request timed out"))
        return


    def _receiveCb(self, transportObj, address, wholeMsg):
        """ Receive response PDU and callback deferred with extracted variable bindings """


        d, transportObj.dObj = transportObj.dObj, None
        err = None
        data = []

        #Decode request message from self.reqMsg
        reqMsg, _ = decoder.decode(
            self.reqMsg, asn1Spec=self.apiVersion.Message())
        #Extract request PDU
        reqPDU = self.apiVersion.apiMessage.getPDU(reqMsg)

        while wholeMsg:
            rspMsg, wholeMsg = decoder.decode(
                wholeMsg, asn1Spec=self.apiVersion.Message())
            rspPDU = self.apiVersion.apiMessage.getPDU(rspMsg)

            # Match response to request
            if self.apiVersion.apiPDU.getRequestID(reqPDU) == self.apiVersion.apiPDU.getRequestID(rspPDU):
                # Check for SNMP errors reported
                errorStatus = self.apiVersion.apiPDU.getErrorStatus(rspPDU)
                if errorStatus:
                    err = Exception(errorStatus.prettyPrint())

                else:
                    for oid, val in self.apiVersion.apiPDU.getVarBinds(rspPDU):
                        if type(val) is NoSuchObject:
                            err = Exception("noSuchName")
                        elif type(val) is EndOfMibView:
                            err = Exception("EndOfMibView")
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
        d.addCallbacks(extract, lambda x: x.getErrorMessage())
        self.transportObj.dObj = d

        self.transportObj.sendMessage(msg, self.target)
        reactor.callLater(5, self._timeoutCb)

        res = yield d
        defer.returnValue(res)

    @defer.inlineCallbacks
    def get(self, oids):

        msg = self._buildMsg(oids, GET)

        res = yield self.send(msg)
        if type(res) is list:
            res = to_names(to_json(res))
        res = response(self.version, self.community, "get", res)

        self.transportObj.closeTransport()
        print res
        defer.returnValue(res)

    @defer.inlineCallbacks
    def set(self, oids):

        msg = self._buildMsg(oids, SET)

        res = yield self.send(msg)
        if type(res) is list:
            res = to_names(to_json(res))
        res = response(self.version, self.community, "set", res)

        self.transportObj.closeTransport()
        print res
        defer.returnValue(res)

    @defer.inlineCallbacks
    def next_one(self, oids):

        msg = self._buildMsg(oids, GET_NEXT)
        res = yield self.send(msg)
        defer.returnValue(res)

    @defer.inlineCallbacks
    def get_next(self, oids):

        res = []
        check = oids[0]
        data = yield self.next_one(oids)

        if type(data) is not list:
            res = data
        else:
            while True:
                new_ids = [k[0] for k in data]
                if not new_ids[0].startswith(check):
                    break
                res.append(data)
                data = yield self.next_one(new_ids)
            res = [to_names(to_json(element)) for element in res]

        res = response(self.version, self.community, "get_next", res)

        self.transportObj.closeTransport()
        print res
        defer.returnValue(res)


def main():

    try:
        fields = from_file()
        arguments = get_arguments(fields['variables'])
        check(arguments, fields['operation'])
        snmp = SNMP(fields['version'], fields['community'], IP, PORT)
    except Exception, e:
        print response(fields['version'], fields['community'], fields['operation'], e.message)
    else:
        if fields['operation'] == 'get':
            op = snmp.get
        elif fields['operation'] == 'get_next':
            op = snmp.get_next
        elif fields['operation'] == 'set':
            op = snmp.set
        else:
            raise Exception, "Operation not supported"

        reactor.callWhenRunning(op, arguments)
        reactor.run()


if __name__ == '__main__':
    main()
