def manageCode(input):

    expressions = []

    string = ""
    cont  = 0

    for char in input:
        if char == "\n":
            pass
        elif char == ";" and cont == 0:
            expressions.append(string+";")
            string = ""
        elif char == "{":
            string += char
            cont+=1
        elif char == "}":
            string += char
            cont-=1
        else:
            string += char
    expressions.append(string)

    return expressions
