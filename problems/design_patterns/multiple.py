class ElectronicDevice(object):

    def __init__(self, name):
        self.name = name

    def power_on(self):
        print "Powered on", self.name

    def power_off(self):
        print "Powered off", self.name

class MusicPlayer(object):

    def __init__(self,name):
        self.name = name

    def play(self):
        print "Playing", self.name

    def stop(self):
        print "Stopped", self.name

class MP3Player(ElectronicDevice, MusicPlayer):

    def __init__(self, name):
        self.name = name
