""" What is the value of the first triangle number
     to have over five hundred divisors? """


def divisors(n):
    """ Returns number of divisors for n
        No checks for bad input to boost efficiency """

    count = 0
    upper = int(n**0.5)+1

    for i in xrange(1,upper):
        if n%i == 0:
           count+=2
        if i*i == n:
           count-=1

    return count

def match(n):
    """ Returns first triangular number with over n divisors
        No checks for bad input to boost efficiency"""
    current = 1
    step = 2

    while True:
        if divisors(current)>n:
           break
        else:
           current += step
           step += 1

    return current

def main():
    """ Compute answer for problem and see how long it takes """

    from time import time
    start = time()
    answer = match(500)
    duration = time() - start
    print answer
    print "Took", duration, "seconds"

if __name__ == '__main__':
    main()
