""" Find the missing term in an Arithmetic Progression """


def find_missing(sequence):
    largest = 0
    smallest = sequence[1]-sequence[0]
    index = 0

    for i in range(len(sequence)-1):
        current = sequence[i+1]-sequence[i]

        if abs(current)>abs(largest):
            largest = current
            index = i

        if abs(current)<abs(smallest):
            smallest = current

    missing = sequence[index]+smallest
    return missing
