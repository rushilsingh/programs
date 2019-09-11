""" write a function maskify, which changes all but the
    last four characters into '#'."""


def maskify(cc):

    last = cc[-4:]
    first = cc[:-4]
    masked = ""
    for char in first:
        masked += "#"
    masked += last
    return masked
