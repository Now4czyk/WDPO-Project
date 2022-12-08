import cv2 as cv
import numpy as np


def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H - 1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)


def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H + 1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)


def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S - 1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)


def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S + 1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)


def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V - 1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)


def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V + 1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)


def on_erosion_trackbar(val):
    global eroMatSize
    eroMatSize = val
    cv.setTrackbarPos('eroMatSize', window_detection_name, eroMatSize)


def on_dilation_trackbar(val):
    global dilMatSize
    dilMatSize = val
    cv.setTrackbarPos('dilMatSize', window_detection_name, dilMatSize)


def on_close_trackbar(val):
    global closeMatSize
    closeMatSize = val
    cv.setTrackbarPos('closeMatSize', window_detection_name, closeMatSize)


def on_open_trackbar(val):
    global openMatSize
    openMatSize = val
    cv.setTrackbarPos('openMatSize', window_detection_name, openMatSize)


def setValues(img, img_resized, img_path, low_H, low_S, low_V, high_H, high_S, high_V, max_value_H, max_value):
    cv.namedWindow(window_detection_name, cv.WINDOW_NORMAL)
    cv.createTrackbar('er', window_detection_name, 0, 15, on_erosion_trackbar)
    cv.createTrackbar('dil', window_detection_name, 0, 15, on_dilation_trackbar)
    cv.createTrackbar('cl', window_detection_name, 0, 15, on_close_trackbar)
    cv.createTrackbar('op', window_detection_name, 0, 15, on_open_trackbar)
    cv.createTrackbar(low_H_name, window_detection_name, low_H, max_value_H, on_low_H_thresh_trackbar)
    cv.createTrackbar(high_H_name, window_detection_name, high_H, max_value_H, on_high_H_thresh_trackbar)
    cv.createTrackbar(low_S_name, window_detection_name, low_S, max_value, on_low_S_thresh_trackbar)
    cv.createTrackbar(high_S_name, window_detection_name, high_S, max_value, on_high_S_thresh_trackbar)
    cv.createTrackbar(low_V_name, window_detection_name, low_V, max_value, on_low_V_thresh_trackbar)
    cv.createTrackbar(high_V_name, window_detection_name, high_V, max_value, on_high_V_thresh_trackbar)

    red = 0
    yellow = 0
    green = 0
    purple = 0

    while True:
        if img is None:
            break

        frame_HSV = cv.cvtColor(img_resized, cv.COLOR_BGR2HSV)
        low_H = cv.getTrackbarPos(low_H_name, window_detection_name)
        low_V = cv.getTrackbarPos(low_V_name, window_detection_name)
        low_S = cv.getTrackbarPos(low_S_name, window_detection_name)
        high_H = cv.getTrackbarPos(high_H_name, window_detection_name)
        high_S = cv.getTrackbarPos(high_S_name, window_detection_name)
        high_V = cv.getTrackbarPos(high_V_name, window_detection_name)
        er = cv.getTrackbarPos('er', window_detection_name)
        dil = cv.getTrackbarPos('dil', window_detection_name)
        op = cv.getTrackbarPos('op', window_detection_name)
        cl = cv.getTrackbarPos('cl', window_detection_name)

        frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))

        erKer = np.ones((er, er), np.uint8)
        dilKer = np.ones((dil, dil), np.uint8)
        clKer = np.ones((cl, cl), np.uint8)
        opKer = np.ones((op, op), np.uint8)

        erosion = cv.erode(frame_threshold, erKer, iterations=1)
        dilation = cv.dilate(erosion, dilKer, iterations=1)
        closing = cv.morphologyEx(dilation, cv.MORPH_CLOSE, clKer)
        opening = cv.morphologyEx(closing, cv.MORPH_OPEN, opKer)

        # counting contours
        contours, hierarchy = cv.findContours(opening, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # cv.drawContours(img_resized, contours, -1, (255, 0, 255), 2)

        # displaying photos
        cv.imshow('final ' + img_path, opening)
        cv.imshow(img_path, img_resized)

        key = cv.waitKey(1)
        if key == ord('q') or key == 27:
            print('=====================================')
            print(len(contours))
            red = len(contours)
            break

    cv.destroyAllWindows()

    return red, green, yellow, purple


window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
