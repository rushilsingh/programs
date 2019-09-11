""" What is the millionth lexicographic permutation of
    the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9? """
TARGET = 1000000

def list_perms(*args):
    """ Return list of permuations from tuple arguments
        Assume good input for efficiency  """

    from itertools import permutations
    perms = list(permutations(args))
    return perms


def main():
    """ Compute answer to problem as see how long it takes """

    from time import time
    start = time()
    perm = list_perms(0,1,2,3,4,5,6,7,8,9)[TARGET-1] #Target element
    answer = int("".join(str(i) for i in perm)) #Convert tuple to int
    duration = time() - start
    print answer
    print "Took", duration, "seconds"

if __name__ == '__main__':
    main()
