class Room(object):

    def __init__(self, *args):

        self.people = []
        if args is not None:
            for arg in args:
                if type(arg) is not str:
                    raise TypeError, "Type must be string"
                self.people.append(arg)
        print "Room initialized"

    def __del__(self):

        print "Room destroyed."

    def __repr__(self):
        result = "Room with "+str(len(self))+" people"
        return result

    def __add__(self, person):
        if type(person) is not str:
            raise TypeError, "Type must be string"

        if person not in self.people:
            self.people.append(person)

    def __sub__(self, person):
        if type(person) is not str:
            raise TypeError, "Type must be string"

        if person in self.people:
            self.people.remove(person)
        else:
            raise LookupError, "Not found"

    def __len__(self):
        return len(self.people)

    def __iter__(self):
        for i in range(len(self)):
            yield self.people[i]

    def __contains__(self, person):
        if person in self.people:
            print "Yes"
            return True
        else:
            print "No"
            return False

    def __eq__(self, other):
        if self.people == other.people:
            return True
        else:
            return False
    def __ne__(self, other):
        return not (self==other)
