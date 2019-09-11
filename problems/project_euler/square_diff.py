""" Find the difference between the sum of the squares of the
     first one hundred natural numbers and the square of the sum."""

def sum_of_square(n):
    total = 0
    for i in xrange(1,n+1):
        total += i*i
    return total

def square_of_sum(n):
    total = sum(xrange(1,n+1))
    result = total * total
    return result

def diff(n):
    result = square_of_sum(n) - sum_of_square(n)
    return result

def main():
    print diff(100)

if __name__ == '__main__':
    main()



