""" Program to check if two words are anagrams """

def count(word):
    """ Create a dictionary from the word in which
        characters are keys and their counts are values. """

    word = word.lower()
    counts = {}
    for char in word:
        counts[char] = counts.get(char, 0)+1
    return counts

def is_anagram(a, b):
    """Check if a and b are anagrams by comparing character counts """

    return count(a) == count(b)

def main():

    assert is_anagram("hello", "olelh")
    assert not is_anagram("heel", "hell")

if __name__ == '__main__':
    main()


