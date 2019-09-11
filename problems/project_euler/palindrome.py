""" Find the largest palindrome made from
    the product of two 3-digit numbers. """

def is_palindrome(number):
    """ Checks if number is a palindrome """
    digits = str(number)
    mid = (len(digits)/2)+1
    for i in range(mid):
         if digits[i] != digits[-(i+1)]:
             return False
    return True

def largest_palindrome():
    """ Find largest palindrome that is the product
        of two three digit numbers """
    largest = 0
    for i in range(999,100, -1):
        for j in range(999,100,-1):
            current = i*j
            if is_palindrome(current) and current>largest:
                largest = current
    return largest

def main():
    from time import time
    start = time()
    answer = largest_palindrome()
    duration = time() - start
    print answer
    print "Took", duration, "seconds"

if __name__ == '__main__':
    main()


