import json
from pathlib import Path
from typing import Dict

import click
import cv2 as cv
from tqdm import tqdm

# MYCODE START ===================================================================================
# from utils.compareJSONs import compareJSONs
# from utils.compareJSONsForAll import compareJSONsForAll
# from utils.TEST_ONE import test
# from utils.TEST_ALL import test_all
import numpy as np

# from utils.SET_VALUES import setValues

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

# PARAMS TO TEST_ONE
max_value = 255
max_value_H = 360 // 2
low_H = lHR
low_S = lSR
low_V = lVR
high_H = hHR
high_S = hSR
high_V = hVR
er = 3
dil = 10
cl = 0
op = 0


# TEMPORARY START =====================================================================================================================

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

        # cv.waitKey(1)
        properContours = len(contours)
        break

    return properContours


def test_all(img, img_resized, lHG, lSG, lVG, hHG, hSG, hVG, eG, dG, cG, oG, lHY, lSY, lVY, hHY, hSY, hVY, eY, dY, cY,
             oY, lHR, lSR, lVR, hHR, hSR, hVR, eR, dR, cR, oR, lHP, lSP, lVP, hHP, hSP, hVP, eP, dP, cP, oP):
    green = test(img, img_resized, lHG, lSG, lVG, hHG, hSG, hVG, eG, dG, cG, oG)
    yellow = test(img, img_resized, lHY, lSY, lVY, hHY, hSY, hVY, eY, dY, cY, oY)
    red = test(img, img_resized, lHR, lSR, lVR, hHR, hSR, hVR, eR, dR, cR, oR)
    purple = test(img, img_resized, lHP, lSP, lVP, hHP, hSP, hVP, eP, dP, cP, oP)
    return green, yellow, red, purple


# TEMPORARY FINISH =====================================================================================================================


# MYCODE FINISH ===================================================================================
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
    # img = cv.imread(img_path, cv.IMREAD_COLOR)
    img_resized = cv.resize(img, None, fx=0.2, fy=0.2)
    # if img_path == 'data\\00.jpg':
    #     img_resized = cv.resize(img, None, fx=0.7, fy=0.7)

    # TODO: Implement detection method.

    # MYCODE START ===================================================================================

    # SETTING VALUES
    # red, green, yellow, purple = setValues(img, img_resized, img_path, low_H, low_S, low_V, high_H, high_S, high_V,
    #                                        max_value_H, max_value)

    # TESTING ONE
    # red = 0
    # green = 0
    # yellow = 0
    # purple = 0
    # red = test(img, img_resized, low_H, low_S, low_V, high_H, high_S, high_V, er, dil, cl, op)
    # TESTING ALL
    green, yellow, red, purple = test_all(img, img_resized, lHG, lSG, lVG, hHG, hSG, hVG, eG, dG, cG, oG, lHY, lSY, lVY,
                                          hHY, hSY, hVY, eY, dY, cY, oY, lHR, lSR, lVR, hHR, hSR, hVR, eR, dR, cR, oR,
                                          lHP, lSP, lVP, hHP, hSP, hVP, eP, dP, cP, oP)

    # MYCODE FINISH ===================================================================================

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

    # MYCODE START ===================================================================================

    # compare jsons and print results to console
    # f1 = open('./utils/properResultValues.json')
    # f2 = open('./result.json')
    # properResults = json.load(f1)
    # results = json.load(f2)
    # # compareJSONs(results, properResults, 'red')
    # compareJSONsForAll(results, properResults)

    # MYCODE FINISH ===================================================================================


if __name__ == '__main__':
    main()
