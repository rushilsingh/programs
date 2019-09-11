

def d_sum(n):
    """ Sum of proper divisors of n.
        Assumes good input to boost efficiency"""

    p_div = set()
    p_div.add(1)

    for i in xrange(2, int(n**0.5)+1):
        if n%i == 0:
            p_div.add(i)
            p_div.add(n/i)

    total = sum(p_div)
    return total

def sum_amicable(n):
    """ Sum of all amicable numbers less than n
        Only numbers over 1 are candidates
        as 1 has no proper divisors  """
    total = 0
    for a in xrange(2,n):
        b = d_sum(a)
        if a!=b and b<n and a == d_sum(b):
            total += a
    return total

def main():
    from time import time
    start = time()
    answer = sum_amicable(10000)
    duration = time() - start
    print answer
    print "Took", duration, "seconds"

if __name__ == '__main__':
    main()

