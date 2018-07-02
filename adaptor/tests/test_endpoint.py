import unittest
import sys
sys.path.insert(0, '/home/username/programs')
from adaptor.endpoint import Endpoint


class Endpoint_Tests(unittest.TestCase):

    def test_endpoint_creation(self):
        
        try:
            ep = Endpoint("172.23.106.217", 22, "ssh", "username:password", 1)
        except:
            self.fail("Failed to instantiate endpoint")    


def main():
    unittest.main()


if __name__ == '__main__':
    main()
