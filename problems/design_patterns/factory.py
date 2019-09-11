class Vehicle(object):

    def factory(type):
        if type == "Car":
            return Car()
        if type == "Bicycle":
            return Bicycle()
        if type == "Plane":
            return Plane()
    factory = staticmethod(factory)

class Car(Vehicle):

    def operate(self):
        print "Driving car"

class Bicycle(Vehicle):

    def operate(self):
        print "Riding bicycle"

class Plane(Vehicle):

    def operate(self):
        print "Flying plane"



