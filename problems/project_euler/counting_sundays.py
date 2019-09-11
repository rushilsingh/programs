""" How many Sundays fell on the first of the month during
    the twentieth century (1 Jan 1901 to 31 Dec 2000)? """

from datetime import date

def sundays_century():
    """ Return number of Sundays on the
        first of the month in the twentieth century """

    count = 0
    for year in xrange(1901,2001):
        for month in xrange(1,13):
            if date(year,month,1).weekday() == 6:
                count += 1

    return count

def main():
    """Compute answer to problem and see how long it takes"""

    from time import time

    start = time()
    answer = sundays_century()
    duration = time() - start

    print answer
    print "Took", duration,"seconds"

if __name__ == '__main__':
    main()
