""" Capitalize each word in a string """


def capitalize(string):
    split_string = string.split(" ")
    result = [word[:1].upper()+word[1:] for word in split_string]
    result = " ".join(result)
    return result


def main():

    assert capitalize("hello world") == "Hello World"
    assert capitalize("convert this") == "Convert This"


if __name__ == '__main__':
    main()
