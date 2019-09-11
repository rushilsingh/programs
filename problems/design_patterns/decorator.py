def decorator(function):
    def _decorator():
        print "Decorating.."
        function()
        print "Decorated."
    return _decorator

@decorator
def simple():
    print "I am a simple function"

def main():

    simple()

if __name__ == '__main__':
    simple()
