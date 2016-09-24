#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time
from calibration import Calibrator, Colors

mirror_mode = True  # flips horizontally
debug_mode = False  # draws all contours

# key pressed (used to escape screen and close)
key = 0

# read stream from a webcam
capture = cv2.VideoCapture(0)

# throws count
counting = 0

# green line
line_height = 240

visible = False  # is the ball in view?
below = False    # under the line?
over = False     # or over it?

# moment of the last counting
last_time = time.time()

# BGR
b, g, r = 0, 0, 80
min_target_color = np.array([b, g, r])
bm, gm, rm = 30, 30, 255
max_target_color = np.array([bm, gm, rm])

colors = Colors(b,g,r,bm,gm,rm)
cal = Calibrator()

while key != 27 and key != 1048603:  # ESC key
    if key != -1: print key

    _, im = capture.read()

    if key == 1048676:  # 'd' (debug)
        debug_mode = not debug_mode

    if key == 99 or key == 1048675:  # 'c' (calibrate)
        print min_target_color
        print max_target_color
        colors = cal.calibrate(im, colors)
        b, g, r = colors.colors['min']
        min_target_color = np.array([b,g,r])
        bm, gm, rm = colors.colors['max']
        max_target_color = np.array([bm,gm,rm])
        print min_target_color
        print max_target_color

    if mirror_mode:
        cv2.flip(im, 1, im)

    # filters out what is not red
    mask = cv2.inRange(im, min_target_color, max_target_color)

    # contours all the red objects found
    contours, _ = cv2.findContours(mask,
                                   cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
    if debug_mode:
        cv2.drawContours(im, contours, -1, (255,255,255), 3)

    # draws green line
    cv2.line(im,
             (0, line_height), (800, line_height),
             (0, 255, 0),  # green
             thickness=3)

    # rectangles
    for contour in contours:
        if cv2.contourArea(contour) > 200:  # only larger objects
            visible = True
            ret_x, ret_y, ret_w, ret_h = cv2.boundingRect(contour)
            cv2.rectangle(im, (ret_x, ret_y),
                              (ret_x+ret_w,
                               ret_y+ret_h),
                              (0, 255, 255), 2)

    # where's the ball
    if visible:
        if ret_y < line_height:
            over = True
        else:
            below = True
            over = False

    # counts
    if over and below:
        if time.time() - last_time > 4:  # 4 seconds to reset
            counting = 0
        counting += 1
        last_time = time.time()
        over = False
        below = False

    # shows counting
    cv2.putText(im,
                '%02d' % counting,
                (500, 70),
                cv2.FONT_HERSHEY_TRIPLEX, 3, (255, 0, 0))

    cv2.imshow('Result', im)

    key = cv2.waitKey(10)

# if __name__ == '__main__':
#     cal = Calibrator()
#     print cal.calibrate(im)
