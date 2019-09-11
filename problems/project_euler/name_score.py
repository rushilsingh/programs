"""
Using names.txt, a 46K text file containing over five-thousand
first names, begin by sorting it into alphabetical order.
Then working out the alphabetical value for each name, multiply this
value by its alphabetical position in the list to obtain a name score.

What is the total of all the name scores in the file?
"""

import string

def listify(fname):
    """ Convert file with names wrapped in quotes and
        separated by commas into sorted list of names """

    with open(fname) as f:
        text = f.read()
    names = text.split(',')  #separate names into list
    names = [name[1:-1] for name in names]  #remove enclosign quotes
    names.sort()
    return names

def alpha_value(name):
    """ Convert individual names into alphabetical values
        based on the characters they contain """
    total = 0
    for char in name:
        total += (string.uppercase.index(char))+1
    return total

def score(names):
    """ Convert list into score based on
        alphabetical value and indices of elements"""
    values = [alpha_value(name) for name in names]

    total = 0
    for index, value in enumerate(values):
        total += value * (index+1)
    return total

def main():
    """ Compute answer and see how long it takes """
    from time import time
    start = time()
    answer = score(listify("names.txt"))
    duration = time() - start
    print answer
    print "Took", duration, "seconds"

if __name__ == '__main__':
    main()



