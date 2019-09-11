"""2520 is the smallest number that can be divided by each
   of the numbers from 1 to 10 without any remainder.
   What is the smallest positive number that is evenly
    divisible by all of the numbers from 1 to 20? """

def divisible(n):
    """ Check if n is evenly divisible by
        all numbers from 1 to 20 """

    for i in range(1,21):
        if n%i !=0:
            return False
    return True

def smallest_divisible():
    n = 2520
    while True:
        if divisible(n):
            return n
            break
        n += 2520

def main():
    print smallest_divisible()

if __name__ == '__main__':
    main()

