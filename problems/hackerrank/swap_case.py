""" You are given a string . Your task is to swap cases. In other words, convert all lowercase letters to uppercase letters and vice versa. """


def swap_case(s):
    result = ""
    for i in s:
        if i.isupper():
            swap = i.lower()
            result += swap
        elif i.islower():
            swap = i.upper()
            result += swap
        else:
            result +=i
    return result

