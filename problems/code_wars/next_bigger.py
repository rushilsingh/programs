def next_bigger(n):
    """ Find next bigger number with same digits
        If no such number exists, return -1. """

    digits = sorted(str(n))
    if len(digits) == 1:
        return -1
    if list(reversed(sorted(str(n)))) == list(str(n)):
        return -1

    target = n+1
    while (sorted(str(target))!=digits):
        target += 1
    return target


def next_bigger_alt(n):
    """ Alternate method to find next bigger number with same digits
        Returns -1 if no such number exists. """

    if n<=10:
        return -1
    if list(reversed(sorted(str(n)))) == list(str(n)):
        return -1

    from itertools import permutations
    perms = [int("".join(i)) for i in permutations(str(n))]
    perms = [i for i in perms if i>n]
    return min(perms)


def main():
    "Get number as command line argument -> python next_bigger 35"

    from sys import argv
    number = int(argv[1])

    import time
    start = time.time()
    result = next_bigger(number)
    result = "non-existent" if result == -1 else result
    end = time.time()
    diff = end-start
    print "Result is %s. First method took %s seconds" % (result, diff)

    start = time.time()
    result = next_bigger_alt(number)
    result = "non-existent" if result == -1 else result
    end = time.time()
    diff = end-start
    print "Result is %s. First method took %s seconds" % (result, diff)


if __name__ == '__main__':
    main()
