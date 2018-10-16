import unittest
from mock import patch
from mock import MagicMock
import sys
sys.path.insert(0, '/home/username/programs')
from adaptor.api_exception import APIException


class APIException_Tests(unittest.TestCase):

    def test_known_error(self):

        message = "Not found: noSuchName"
        e  = APIException(message)

        self.assertEquals(e._get_code(message), 404)
        self.assertEquals(e.code, 404)

    def test_unclassified_error(self):

        message = "Internal server error: Unclassified Error Message (unclassified error)"
        e = APIException(message)

        self.assertEquals(e._get_code(message), 500)
        self.assertEquals(e.code, 500)

def main():
    unittest.main()


if __name__ == '__main__':
    main()
