class Result:
    status = ""
    messages = []
    fileName = []

    def __init__(self, fn, s, msg):
        self.status = s
        self.fn = fn
        self.messages = msg


def compareJSONs(results, properResults, testedColor):
    messages = []
    for fileName, colors in properResults.items():
        checkFile = []
        for color in colors:
            for myFileName, myColors in results.items():
                if fileName == myFileName:
                    for myColor in myColors:
                        if (myColor == color) & (color == testedColor) & (myColors[myColor] != colors[color]):
                            checkFile.append(f'{color}, should be {colors[color]} but there is {myColors[myColor]}')
        if len(checkFile) == 0:
            messages.append(Result(fileName, 'success', []))
        else:
            messages.append(Result(fileName, 'error', checkFile))

    for message in messages:
        print(f'{message.fn} {message.status}')
        if message.status == 'error':
            for msg in message.messages:
                print(msg)
