class A:

    def __getitem__(self, index):
        if index>11:
            raise IndexError, "No more items"
        else:
            return index*11
class B:

    def __iter__(self):
        yield 11
        yield 22
        yield 33


