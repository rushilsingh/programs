""" Find the sum of all the primes below two million. """

def is_prime(n):

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

def sum_primes(target):

    if target<2:
       return 0
    if target==2:
       return 2
    total = 2
    current = 3
    while True:
        if current>=target: break
        if is_prime(current):
            total+=current
        current+=2
    return total

def main():
    from time import time
    start = time()
    print sum_primes(2000000)
    duration = time() - start
    print "Took", duration, "seconds"

if __name__ == '__main__':
    main()

