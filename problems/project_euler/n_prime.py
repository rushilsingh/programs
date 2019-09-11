
def is_prime(n):
    """ Find if number is prime """
    if n < 2:
         return False
    if n % 2 == 0:
         return n == 2
    k = 3
    while k*k <= n: #non-primes have factor <= their square root
         if n % k == 0:
             return False
         k += 2 #only odd numbers are prime
    return True

def n_prime(n):
    """ Find the nth prime number """
    if n<1:
       raise ValueError, "Invalid"
    if n == 1:
        return 2
    count = 1
    current = 3
    while True:
        if is_prime(current):
            count += 1
        if count == n:
            return current
            break
        current += 2 #only odd numbers are prime

def main():
    from time import time
    start = time()
    print n_prime(10001)
    #print n_prime(100000)
    duration = time() - start
    print "Took", duration, "seconds"

if __name__ == '__main__':
    main()
