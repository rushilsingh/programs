""" What is the sum of the digits of the number 2^1000? """

def digit_sum(number):

    return sum([int(digit) for digit in str(number)])

def main():

    from time import time

    start = time()
    print digit_sum(2**1000)
    duration = time() - start
    print "Took", duration, "seconds"

if __name__ == '__main__':
    main()

