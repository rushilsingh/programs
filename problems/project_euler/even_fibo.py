""" By considering the terms in the Fibonacci sequence
    whose values do not exceed 4 million find the sum
    of the even-valued terms. """

def fibo(n):
    """ Return a list of fibonacci numbers with values upto n"""
    seq = []
    first = 0
    second = 1
    while True:
        if first>n:
            break
        seq.append(first)
        first, second = second, first+second
    return seq

def even_sum(seq):
    """ Returns the sum of the even valued terms in a sequence """
    return sum([i for i in seq if i%2==0])

def main():
    """ Computes solution to problem and
        checks how long it takes """
    from time import time
    start = time()
    answer = even_sum(fibo(4000000))
    duration = time() - start
    print answer
    print "Took", duration, "seconds"


if __name__ == '__main__':
    main()
