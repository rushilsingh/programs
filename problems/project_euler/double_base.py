""" Find the sum of all numbers, less than one million,
    which are palindromic in base 10 and base 2. """
TARGET = 1000000

def is_palindrome(digits):
    """ Checks if string representation of number is a palindrome """
    mid = (len(digits)/2)+1
    for i in range(mid):
         if digits[i] != digits[-(i+1)]:
             return False
    return True

def sum_both(n):
    """ Finds the sum of all numbers >=1 and <n
        which are palindromic in both bases. """
    total = 0
    for i in xrange(1,n):
        if is_palindrome(str(i)) and is_palindrome("{0:b}".format(i)):
            total += i

    return total

def main():
    """ Computes answer and checks how long it takes """
    from time import time
    start = time()
    answer = sum_both(TARGET)
    duration = time() - start
    print answer
    print "Took", duration, "seconds"

if __name__ == '__main__':
    main()
