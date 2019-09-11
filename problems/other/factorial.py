""" Find factorial of number with and without recursion """


TARGET = 10000

def factorial(number):
    """ Find factorial of a number """
    if number < 0:
        raise ValueError, "Number must be positive"
    elif number<=1:
        return 1
    else:
        result = 1
        for i in xrange(1, number+1):
            result *= i
        return result


def factorial_recursive(number):
   """ Find factorial of a number recursively """
   if number<0:
       raise ValueError, "Please provide positive integer"
   elif number<=1:
        return 1
   else:
        return number*factorial(number-1)




def main():
    """ Check correctness of factorial functions.
        Compare times between the two versions. """

    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(2) == 2
    assert factorial(5) == 120
    assert factorial_recursive(6) == 720
    assert factorial(10) == 3628800
    assert factorial_recursive(10) == 3628800

    from time import time

    start = time()
    answer = factorial(TARGET)
    duration1 = time() - start
    start = time()
    answer = factorial_recursive(TARGET)
    duration2 = time() - start
    print "Non-recursive took", duration1, "seconds"
    print "Recursive took", duration2, "seconds"
    if duration1>duration2:
        print "Recursive version is faster"
    elif duration1<duration2:
        print "Non-recursive version is faster"
    else:
        print "Both versions take exactly the same time"



if __name__ == '__main__':
    main()
