import json
from pathlib import Path
from typing import Dict

import click
import cv2 as cv
from tqdm import tqdm
import numpy as np

# Variables for color recognition settings
# GREEN
lHG = 36
hHG = 51
lSG = 195
hSG = 255
lVG = 137
hVG = 245
eG = 1
dG = 9
cG = 0
oG = 0

# RED
lHR = 174
hHR = 179
lSR = 174
hSR = 226
lVR = 108
hVR = 215
eR = 3
dR = 10
cR = 0
oR = 0

# PURPLE
lHP = 162
hHP = 176
lSP = 0
hSP = 235
lVP = 0
hVP = 121
eP = 0
dP = 0
cP = 13
oP = 0

# YELLOW
lHY = 20
hHY = 26
lSY = 153
hSY = 255
lVY = 100
hVY = 255
eY = 5
dY = 4
cY = 0
oY = 0


# params test one color
# max_value = 255
# max_value_H = 360 // 2
# low_H = lHR
# low_S = lSR
# low_V = lVR
# high_H = hHR
# high_S = hSR
# high_V = hVR
# er = 3
# dil = 10
# cl = 0
# op = 0


# Function that tests one color recognition
def test(img, img_resized, low_H, low_S, low_V, high_H, high_S, high_V, er, dil, cl, op):
    properContours = 0

    while True:
        if img is None:
            break

        frame_HSV = cv.cvtColor(img_resized, cv.COLOR_BGR2HSV)
        frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))

        erosion = cv.erode(frame_threshold, np.ones((er, er), np.uint8), iterations=1)
        dilation = cv.dilate(erosion, np.ones((dil, dil), np.uint8), iterations=1)
        closing = cv.morphologyEx(dilation, cv.MORPH_CLOSE, np.ones((cl, cl), np.uint8))
        opening = cv.morphologyEx(closing, cv.MORPH_OPEN, np.ones((op, op), np.uint8))

        contours, hierarchy = cv.findContours(opening, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        properContours = len(contours)
        break

    return properContours


# Function that tests all colors recognition
def test_all(img, img_resized, lHG, lSG, lVG, hHG, hSG, hVG, eG, dG, cG, oG, lHY, lSY, lVY, hHY, hSY, hVY, eY, dY, cY,
             oY, lHR, lSR, lVR, hHR, hSR, hVR, eR, dR, cR, oR, lHP, lSP, lVP, hHP, hSP, hVP, eP, dP, cP, oP):
    green = test(img, img_resized, lHG, lSG, lVG, hHG, hSG, hVG, eG, dG, cG, oG)
    yellow = test(img, img_resized, lHY, lSY, lVY, hHY, hSY, hVY, eY, dY, cY, oY)
    red = test(img, img_resized, lHR, lSR, lVR, hHR, hSR, hVR, eR, dR, cR, oR)
    purple = test(img, img_resized, lHP, lSP, lVP, hHP, hSP, hVP, eP, dP, cP, oP)
    return green, yellow, red, purple


def detect(img_path: str) -> Dict[str, int]:
    """Object detection function, according to the project description, to implement.

    Parameters
    ----------
    img_path : str
        Path to processed image.

    Returns
    -------
    Dict[str, int]
        Dictionary with quantity of each object.
    """
    img = cv.imread(img_path, cv.IMREAD_COLOR)
    img_resized = cv.resize(img, None, fx=0.2, fy=0.2)

    # Implementation

    # Settings for testing one color recognition
    # red = 0
    # green = 0
    # yellow = 0
    # purple = 0
    # red = test(img, img_resized, low_H, low_S, low_V, high_H, high_S, high_V, er, dil, cl, op)

    # Settings for testing all colors recognition
    green, yellow, red, purple = test_all(img, img_resized, lHG, lSG, lVG, hHG, hSG, hVG, eG, dG, cG, oG, lHY, lSY, lVY,
                                          hHY, hSY, hVY, eY, dY, cY, oY, lHR, lSR, lVR, hHR, hSR, hVR, eR, dR, cR, oR,
                                          lHP, lSP, lVP, hHP, hSP, hVP, eP, dP, cP, oP)

    return {'red': red, 'yellow': yellow, 'green': green, 'purple': purple}


@click.command()
@click.option('-p', '--data_path', help='Path to data directory',
              type=click.Path(exists=True, file_okay=False, path_type=Path), required=True)
@click.option('-o', '--output_file_path', help='Path to output file', type=click.Path(dir_okay=False, path_type=Path),
              required=True)
def main(data_path: Path, output_file_path: Path):
    img_list = data_path.glob('*.jpg')

    results = {}
    for img_path in tqdm(sorted(img_list)):
        fruits = detect(str(img_path))
        results[img_path.name] = fruits

    with open(output_file_path, 'w') as ofp:
        json.dump(results, ofp)

    # Code snippet for colors recognition tests. It involves jsons comparing and printing results to console
    # f1 = open('./utils/properResultValues.json')
    # f2 = open('./result.json')
    # properResults = json.load(f1)
    # results = json.load(f2)
    # compareJSONs(results, properResults, 'red')
    # compareJSONsForAll(results, properResults)


if __name__ == '__main__':
    main()

# Util for comparing JSONs for one color recognition
# class Result:
#     status = ""
#     messages = []
#     fileName = []
#
#     def __init__(self, fn, s, msg):
#         self.status = s
#         self.fn = fn
#         self.messages = msg
#
# def compareJSONs(results, properResults, testedColor):
#     messages = []
#     for fileName, colors in properResults.items():
#         checkFile = []
#         for color in colors:
#             for myFileName, myColors in results.items():
#                 if fileName == myFileName:
#                     for myColor in myColors:
#                         if (myColor == color) & (color == testedColor) & (myColors[myColor] != colors[color]):
#                             checkFile.append(f'{color}, should be {colors[color]} but there is {myColors[myColor]}')
#         if len(checkFile) == 0:
#             messages.append(Result(fileName, 'success', []))
#         else:
#             messages.append(Result(fileName, 'error', checkFile))
#
#     for message in messages:
#         print(f'{message.fn} {message.status}')
#         if message.status == 'error':
#             for msg in message.messages:
#                 print(msg)

# Utils for comparing JSONs for all colors recognition
# class Result:
#     status = ""
#     messages = []
#     colors = []
#
#     def __init__(self, fn, s, msg):
#         self.status = s
#         self.fn = fn
#         self.messages = msg
#
# def compareJSONsForAll(results, properResults):
#     messages = []
#     baseError = 0
#
#     for fileName, colors in properResults.items():
#         checkFile = []
#         for color in colors:
#             for myFileName, myColors in results.items():
#                 if fileName == myFileName:
#                     sum = colors['yellow'] + colors['green'] + colors['purple'] + colors['red']
#                     for myColor in myColors:
#                         if (myColor == color) & (myColors[myColor] != colors[color]):
#                             checkFile.append(f'{color}, should be {colors[color]} but there is {myColors[myColor]}')
#                             baseError += abs(colors[color] - myColors[myColor]) / sum
#
#         if len(checkFile) == 0:
#             messages.append(Result(fileName, 'success', []))
#         else:
#             messages.append(Result(fileName, 'error', checkFile))
#
#     for message in messages:
#         print(f'{message.fn} {message.status}')
#         if message.status == 'error':
#             for msg in message.messages:
#                 print(msg)
#
#     # meanAbsoluteRelativePercentageError
#     errorPercentage = baseError * 100 / 40
#     print(f'error percentage = {errorPercentage}%')
#     print(f'score = {100 - errorPercentage}%')
