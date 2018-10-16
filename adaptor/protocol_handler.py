from abc import ABCMeta, abstractmethod


class Protocol_Handler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, feature_name, *args):
        pass

    @abstractmethod
    def post(self, feature_name, *args):
        pass

    @abstractmethod
    def put(self, feature_name, *args):
        pass

    @abstractmethod
    def delete(self, feature_name, *args):
        pass

    @abstractmethod
    def list(self, feature_name, *args):
        pass


