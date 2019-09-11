""" Find the last ten digits of the series,
    1^1 + 2^2 + 3^3 + ... + 1000^1000. """


def sum_series(n):
    """ Returns total of series described in problem """
    if type(n) is not int:
        raise TypeError, "Only accepts integers"
    if n<1:
        raise ValueError, "Only values of 1 or greater are allowed"

    total = sum([i**i for i in xrange(1, n+1)])
    return total

def last_ten(n):
    """ Returns last 10 digits of a number
        If number has less than 10 digits, returns number """
    digits = str(n)
    last = digits[-10:]
    return int(last)

def main():
    from time import time
    start = time()
    total = sum_series(1000)
    answer = last_ten(total)
    duration = time() - start
    print answer
    print "Took", duration, "seconds"

if __name__ == '__main__':
    main()




