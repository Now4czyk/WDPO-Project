class Result:
    status = ""
    messages = []
    colors = []

    def __init__(self, fn, s, msg):
        self.status = s
        self.fn = fn
        self.messages = msg


def compareJSONsForAll(results, properResults):
    messages = []
    baseError = 0

    for fileName, colors in properResults.items():
        checkFile = []
        for color in colors:
            for myFileName, myColors in results.items():
                if fileName == myFileName:
                    sum = colors['yellow'] + colors['green'] + colors['purple'] + colors['red']
                    for myColor in myColors:
                        if (myColor == color) & (myColors[myColor] != colors[color]):
                            checkFile.append(f'{color}, should be {colors[color]} but there is {myColors[myColor]}')
                            baseError += abs(colors[color] - myColors[myColor]) / sum

        if len(checkFile) == 0:
            messages.append(Result(fileName, 'success', []))
        else:
            messages.append(Result(fileName, 'error', checkFile))

    for message in messages:
        print(f'{message.fn} {message.status}')
        if message.status == 'error':
            for msg in message.messages:
                print(msg)

    # meanAbsoluteRelativePercentageError
    errorPercentage = baseError * 100 / 40
    print(f'error percentage = {errorPercentage}%')
    print(f'score = {100 - errorPercentage}%')
