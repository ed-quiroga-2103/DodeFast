def saveText(text,filename):
    file = open(filename+".txt","w+")

    file.write(text)

    file.close()

    return

def loadText(filename):
    file = open(filename, "r")

    text = file.read()

    file.close()

    return text
