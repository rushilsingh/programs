""" The number, 197, is called a circular prime because all rotations
    of the digits: 197, 971, and 719, are themselves prime.
    There are thirteen such primes below 100:
    2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.
    How many circular primes are there below one million? """

TARGET = 1000000

def rotations(number):
    """ From a number, computes all rotations of the digits"""
    digits = str(number)
    n = len(digits)
    results = []
    for i in range(n):
        results.append(digits)
        digits = digits[1:]+digits[0]
    results = [int(result) for result in results]
    return results

def is_prime(n):
    """ Determines whether a number is prime """

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

def circulars(n):
    """ Determines number of circular primes below n """
    if n<2:
        return 0
    else:
        count = 1 # initialized to 1 as 2 fits criteria
        current = 3 #circular prime after 2
        while (current<n):
            if all(is_prime(num) for num in rotations(current)):
                count += 1
            current += 2
    return count

def main():
    """ Compute answer and see how long it takes """
    from time import time

    start = time()
    answer = circulars(TARGET)
    duration = time() - start
    print answer
    print "Took", duration, "seconds"

if __name__ == '__main__':
    main()
