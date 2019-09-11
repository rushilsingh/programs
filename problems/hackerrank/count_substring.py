""" Write a program to count the number of occurrences
    of a substring in a string """


def count_substring(string, sub_string):
    big = len(string)
    small = len(sub_string)
    count = 0
    for i in xrange(big-small+1):
        match = True
        for j in xrange(small):
            if string[i+j] != sub_string[j]:
                match = False
                break
        if match is True:
            count+=1
    return count


def main():
    assert count_substring("banana", "ana") is 2


if __name__ == '__main__':
    main()
