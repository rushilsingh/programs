""" Find the sum of all numbers which are equal to
    the sum of the factorial of their digits.
    Note: as 1! = 1 and 2! = 2 are not sums they are not included."""


# Pre-calculated upper bound 9!*7
# No possible higher value since 9!*8 is also a 7 digit number
BOUND = 2540160

def fact(n):
    """ Calculates factorial of number """

    if n<=1:
        return 1
    else:
        return n*fact(n-1)

#Compute a list of digit factorials
FAST_FACT = [fact(i) for i in xrange(10)]


def is_equal(n):
    """ Checks if number is equal to
        sum of factorial of digits """

    fact_sum = sum([FAST_FACT[int(i)] for i in str(n)])
    if n == fact_sum:
        return True
    else:
        return False

def sum_all():
    """ Returns sum of all numbers that are equal to
        the sum of the factorial of their digits
        Uses precalculated upper bound
        1 and 2 are excluded as per problem statement """

    total = 0
    for number in range(3,BOUND):
        if is_equal(number):
            total += number
    return total

def main():
    """ Compute answer and see how long it takes """

    from time import time
    start = time()
    answer = sum_all()
    duration = time() - start

    print answer
    print "Took", duration, "seconds"


if __name__ == '__main__':
    main()
