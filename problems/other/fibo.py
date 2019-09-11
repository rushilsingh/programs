""" Generate a fibonacci number series """


def fibo(n):
    """ Generator object with fibonacci series with n terms """
    first = 0
    second = 1
    while n:
        yield first
        first, second = second, first+second
        n -=1

def fibo_recur(n):
    """ Return nth fibonacci number using recursion """

    if n<=1:
        return n
    else:
        return fibo_recur(n-1)+ fibo_recur(n-2)
