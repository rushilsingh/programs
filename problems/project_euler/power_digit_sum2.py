
def digit_sum(number):
    digits = str(number)
    total = 0
    for digit in digits:
        total += int(digit)
    return total

def main():

    from time import time
    start = time()
    print digit_sum(2**1000)
    duration = time() - start
    print "Took", duration, "seconds"

if __name__ == '__main__':
    main()
