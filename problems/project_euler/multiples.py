""" Find the sum of all the multiples of 3 or 5 below 1000 """

def sum_multiples(n):
    sum = 0
    for i in range(n):
        if i%3 == 0:
           sum += i
        elif i%5 == 0:
           sum += i
    return sum

def main():
    print sum_multiples(1000)

if __name__=='__main__':
    main()
