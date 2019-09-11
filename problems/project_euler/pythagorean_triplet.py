"""
A Pythagorean triplet is a set of three natural numbers,
a < b < c, for which, a2 + b2 = c2

For example, 32 + 42 = 9 + 16 = 25 = 52.

There exists exactly one Pythagorean triplet for which
 a + b + c = 1000.Find the product abc.
"""

def is_triplet(a,b,c):
    """ Check if pythagorean triplet """
    if c*c == a*a + b*b:
        return True
    else:
        return False

def find_product():
    """ Find product as defined in problem statement """

    for a in range(1, 1000):
        for b in range(a, 1000 - a):
            c = 1000 - a - b
            if c<b or c<a:
               break
            if is_triplet(a, b, c):
                product = a*b*c
                return product
def main():
    from time import time
    start = time()
    print find_product()
    duration =  time() - start
    print "Took", duration, "seconds"

if __name__ == '__main__':
    main()
