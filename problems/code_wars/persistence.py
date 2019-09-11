""" Write a function, persistence, that takes in a positive parameter
    num and returns its multiplicative persistence, which is the
    number of times you must multiply the digits in num until you
    reach a single digit. """


def persistence(n):
    count = 0
    while (len(str(n))>1):
        digits = [int(i) for i in str(n)]
        res = 1
        for digit in digits:
            res = res*digit
        n = res
        count += 1
    return count
