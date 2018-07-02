import unittest
from mock import patch
from mock import MagicMock
import sys
sys.path.insert(0, "/home/username/programs")
from adaptor import endpoint
from adaptor.endpoints.snmp import snmp
from twisted.internet import defer


class SNMP_Globals_Tests(unittest.TestCase):

    def test_extract_values(self):

        data = [
            (snmp.types['ObjectName']('1.3.6.1.2.1.1'),
             snmp.types['OctetString']('Some Value')),
            (snmp.types['ObjectName']('1.3.6.1.2.1.2'),
             snmp.types['TimeTicks'](100))
        ]
        values = snmp.extract_values(data)
        expected_values = [
            ('1.3.6.1.2.1.1', 'Some Value'),
            ('1.3.6.1.2.1.2', 100)
        ]
        self.assertEquals(values, expected_values)

    def test_to_json(self):

        data = [('1.3.6.1.2.1.1', 'Some Value'), ('1.3.6.1.2.1.2', 100)]
        values = snmp.to_json(data)
        expected_values = {'1.3.6.1.2.1.1': 'Some Value', '1.3.6.1.2.1.2': 100}
        self.assertEquals(values, expected_values)

    def test_to_names(self):

        data = {
            '1.3.6.1.2.1.1.5.0': 'System Name',
            '1.3.6.1.2.1.1.1.0': 'System Description',
            '1.3.6.1.2.1.1.6.0': 'System Location'
        }
        values = snmp.to_names(data, "sysconfig")
        expected_values = {
            'Name': 'System Name',
            'Description': 'System Description',
            'Location': 'System Location'
        }
        self.assertEquals(values, expected_values)

    def test_args_from_feature_get_valid(self):

        oids = snmp.args_from_feature("sysconfig", snmp.GET)
        expected_oids = ['1.3.6.1.2.1.1.5.0',
                         '1.3.6.1.2.1.1.1.0', '1.3.6.1.2.1.1.6.0']
        self.assertEquals(set(oids), set(expected_oids))

    def test_args_from_feature_get_invalid(self):

        with self.assertRaises(KeyError):
            snmp.args_from_feature("invalid_feature", snmp.GET)

    def test_check_for_errors_get_valid(self):

        data = ['1.3.6.1.2.1.1.5.0', '1.3.6.1.2.1.1.1.0', '1.3.6.1.2.1.1.6.0']
        try:
            snmp.check_for_errors(data, snmp.GET)
        except:
            self.fail("Raised exception on valid input")

    def test_check_for_errors_get_invalid_prefix(self):

        data = ['2.4.7.1.2.1.1.5.0', '2.4.7.1.2.1.1.1.0']
        with self.assertRaises(Exception) as cm:
            snmp.check_for_errors(data, snmp.GET)
        self.assertEquals(cm.exception.message, "Bad request: Invalid OID")

    def test_check_for_errors_get_invalid_tabular_not_supported(self):

        data = ['1.3.6.1.2.1.1.4.1', '1.3.6.1.2.1.1.3.1']
        with self.assertRaises(Exception) as cm:
            snmp.check_for_errors(data, snmp.GET)
        self.assertEquals(cm.exception.message,
                          "Method not allowed: Tabular not supported for get")


class SNMP_Tests(unittest.TestCase):

    def setUp(self):
        ep = endpoint.Endpoint('127.0.0.1', 161, 'snmp', "public:private", 1)
        self.snmp = snmp.SNMP(ep)
        # Transport object is mock that does nothing
        self.snmp.transportObj = MagicMock()

    def test_instantiate_valid(self):

        ep1 = endpoint.Endpoint('127.0.0.1', 161, 'snmp', 'public:private', 1)
        ep2 = endpoint.Endpoint('127.0.0.1', 161, 'snmp', 'public:private', 2)

        try:
            snmp1 = snmp.SNMP(ep1)
            snmp2 = snmp.SNMP(ep2)
        except:
            self.fail("Failed to instantiate valid objects")

    def test_instantiate_invalid_version(self):

        ep = endpoint.Endpoint('127.0.0.1', 161, 'snmp', 'public:private', 4)

        with self.assertRaises(Exception) as cm:
            snmp_obj = snmp.SNMP(ep)

        self.assertEquals(cm.exception.message,
                          "Bad request: Version not supported")

    @defer.inlineCallbacks
    def test_get_valid(self):

        @defer.inlineCallbacks
        def mock_send(message):
            d = defer.Deferred()
            d.addCallbacks(snmp.extract_values, lambda x: x.getErrorMessage())
            response = [
                (snmp.types["ObjectName"]('1.3.6.1.2.1.1.5.0'),
                 snmp.types["OctetString"]("System Name")),
                (snmp.types["ObjectName"]('1.3.6.1.2.1.1.1.0'),
                 snmp.types["OctetString"]("System Description")),
                (snmp.types["ObjectName"]('1.3.6.1.2.1.1.6.0'),
                 snmp.types["OctetString"]("System Location"))

            ]
            d.callback(response)
            res = yield d
            defer.returnValue(res)

        self.snmp.send = mock_send
        result = yield self.snmp.get("sysconfig")
        expected_result = {
            'version': 1,
            'credentials': 'public:private',
            'properties': [{
                "Name": "System Name",
                "Description": "System Description",
                "Location": "System Location"
            }]
        }
        self.assertEquals(result, expected_result)

    @defer.inlineCallbacks
    def test_get_invalid_device_returned_error(self):

        @defer.inlineCallbacks
        def mock_send(message):
            d = defer.Deferred()
            d.addCallbacks(snmp.extract_values, lambda x: x.getErrorMessage())
            d.errback(Exception("Internal server error: Something went wrong"))
            res = yield d
            defer.returnValue(res)

        self.snmp.send = mock_send
        result = yield self.snmp.get("sysconfig")
        expected_result = "Internal server error: Something went wrong"
        self.assertEquals(result, expected_result)

    @defer.inlineCallbacks
    def test_get_invalid_feature(self):

        result = yield self.snmp.get("invalid_feature")
        expected_result = "Not found: Feature not found in conf file"
        self.assertEquals(result, expected_result)

    def test_list_not_allowed(self):

        with self.assertRaises(NotImplementedError) as cm:
            self.snmp.list("sysconfig")

        self.assertEquals(
            cm.exception.message, "Method not allowed: SNMP currently supports only GET")

    def test_post_not_allowed(self):

        with self.assertRaises(NotImplementedError) as cm:
            self.snmp.post("sysconfig")

        self.assertEquals(
            cm.exception.message, "Method not allowed: SNMP currently supports only GET")

    def test_put_not_allowed(self):

        with self.assertRaises(NotImplementedError) as cm:
            self.snmp.put("sysconfig")

        self.assertEquals(
            cm.exception.message, "Method not allowed: SNMP currently supports only GET")

    def test_delete_not_allowed(self):

        with self.assertRaises(NotImplementedError) as cm:
            self.snmp.delete("sysconfig")

        self.assertEquals(
            cm.exception.message, "Method not allowed: SNMP currently supports only GET")


def main():
    unittest.main()


if __name__ == '__main__':
    main()
