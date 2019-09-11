

def fact(n):
    """ Calculates factorial of number."""
    if n<0:
        raise ValueError, "Factorial undefined for negative numbers."
    elif n==0:
        return 1
    else:
        return n*fact(n-1)

def digit_sum(n):
    """ Computes sum of digits of n """
    digits = [int(digit) for digit in str(n)]
    return sum(digits)

def main():

    from time import time
    start = time()
    answer = digit_sum(fact(100))
    duration = time() - start
    print answer
    print "Took", duration, "seconds"

if __name__ == '__main__':
    main()
