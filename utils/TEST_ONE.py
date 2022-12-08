import cv2 as cv
import numpy as np


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

        cv.waitKey(1)
        properContours = len(contours)
        break

    return properContours
