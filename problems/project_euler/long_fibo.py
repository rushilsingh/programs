""" What is the index of the first term in the
    Fibonacci sequence to contain 1000 digits? """

def check(n):
    """Check if a number contains atleast thousand digits """
    if len(str(n)) >= 1000:
        return True
    else:
        return False

def match():
    """ Returns index of first term in Fibonacci sequence
        that matches condition """
    first = 0
    second = 1
    index = 1
    while True:
        if check(second):
            break
        first, second = second, first+second
        index +=1
    return index

def main():
    """ Computes answer to problem and checks how long it takes """
    from time import time
    start = time()
    answer = match()
    duration = time() - start
    print answer
    print "Took", duration, "seconds"

if __name__ == '__main__':
    main()
