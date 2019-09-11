"""What is the largest prime factor of a number """

TARGET = 600851475143

def is_prime(n):
    """Find out if a number is prime """
    if n < 2:
         return False
    if n % 2 == 0:
         return n == 2
    k = 3
    while k*k <= n:
         if n % k == 0:
             return False
         k += 2
    return True

def is_perfect(n):
    """ Checks if n is a perfect square """
    sqrt =int(n ** 0.5)
    sq = sqrt * sqrt
    if n == sq:
        return True
    else:
        return False

def efficient_lpf(n):
    """ Find the largest prime factor for a number.
        This algorithm is efficient but
        does not work on small inputs or perfect squares """
    i = 3
    while i*i<n:
        if n%i == 0:
            n = n/i
        i += 2
    return n

def inefficient_lpf(n):
    """ Find the largest prime factor for a number
        This algorithm is inefficient but works on all input"""

    for i in xrange(1, n/2+1):
        if n%i == 0 and is_prime(i):
            largest = i
    return largest

def largest_prime_factor(n):
    """ Find the largest prime factor.
        Pick algorithm based on input. """

    if n<15 or is_perfect(n):
        return inefficient_lpf(n)
    else:
        return efficient_lpf(n)


def main():
    """ Compute answer and see how long it takes """

    from time import time
    start = time()
    print largest_prime_factor(TARGET)
    duration = time() - start
    print "Took", duration, "seconds"

if __name__ == '__main__':

    main()

