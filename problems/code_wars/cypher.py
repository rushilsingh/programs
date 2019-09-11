def rot13(message):
    """ Implement a cypher that rotates character position by 13 """

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    coding = {}
    decoding = {}
    for index, value in enumerate(alphabet):
         coding[value] = index+1
         decoding[index+1] = value
    result = ""
    for char in message:
        if char.lower() not in alphabet:
            result += char
        else:
            code = coding[char.lower()]
            if code<=13:
                code += 13
            else:
                code -= 13
            sub = decoding[code]
            if char.isupper():
                sub = sub.upper()
            result += sub
    return result
