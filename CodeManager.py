def manageCode(input):

    expressions = []

    string = ""
    cont  = 0

    for char in input:
        if char == "\n":
            pass
        else:
            string += char

    expressions.append(string)

    return expressions
