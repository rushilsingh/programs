class Fan(object):

    def power_on(self):
        print "Fan powered on"

    def power_off(self):
        print "Fan powered off"

class Bulb(object):

    def power_on(self):
        print "Bulb powered on"

    def power_off(self):
        print "Bulb powered off"

class Pen(object):

    def open(self):
        print "Opened pen"

    def close(pen):
        print "Closed pen"

class Door(object):

    def open(self):
        print "Opened door"

    def close(self):
        print "Closed door"


class ElectricalDevice(object):

    properties = set(['power_on', 'power_off'])

    def __init__(self, device):
        if str(device).startswith('<class '):
            d = device()
        else:
            d = device

        if set(dir(d)).issuperset(ElectricalDevice.properties):
            self.device = d
        else:
            raise TypeError, "Not an electrical device"

    def __getattr__(self,prop):
        return getattr(self.device, prop)

class Openable(object):

    properties = set(['open', 'close'])

    def __init__(self, device):

        if str(device).startswith('<class '):
            d = device()
        else:
            d = device

        if set(dir(d)).issuperset(Openable.properties):
            self.device = d
        else:
            raise TypeError, "Not an openable device"

    def __getattr__(self, prop):
        return getattr(self.device, prop)

