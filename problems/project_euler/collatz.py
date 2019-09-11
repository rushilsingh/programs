""" Which starting number, under one million,
    produces the longest collatz sequence """

TARGET = 1000000

def collatz(n):
    """ Returns length of collatz sequence when started at n """

    current = n
    seq = [current]
    while True:
        if current == 1:
            break
        elif current%2==0:
            current /= 2
        else:
            current = 3*current + 1
        seq.append(current)

    return len(seq)

def longest_chain(n):
    """ Finds starting number that forms longest collatz sequence
        for all numbers less than n """
    largest = 0
    result = None
    for i in range(1,n):
        c = collatz(i)
        if c>largest:
            largest = c
            result = i
    return result

def main():
    """ Compute answer and see how long it takes """

    from time import time
    start = time()
    answer = longest_chain(TARGET)
    duration = time() - start

    print answer
    print "Took", duration, "seconds"

if __name__ == '__main__':
    main()



