#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import cv2

mirror_mode = True

WINDOW_NAME = "ocarneiro/conta-bolas"

class Juggling(object):

    def __init__(self, capture):
        self.mirror_mode = True
        self.window_name = WINDOW_NAME
        self.capture = capture
        self.get_feed()

    def get_feed(self):
        _, self.image = self.capture.read()
        if self.mirror_mode:
            cv2.flip(self.image, 1, self.image)

    def show(self):
        cv2.imshow(self.window_name, self.image)

# setup webcam
capture = cv2.VideoCapture(0)

j = Juggling(capture)

key = 0

MARGIN_LEFT = 100
MARGIN_TOP = 100
FILLED = -1
INCREMENT = 10
RED = (0,0,255)

r = 200

while key != 27 and key != 1048603:
    j.get_feed()
    cv2.circle(j.image, (MARGIN_LEFT, MARGIN_TOP + r), 10, RED, FILLED)
    j.show()
    key = cv2.waitKey(10)
    if key >= 0:
        if key == 113:
            r += INCREMENT
        if key == 97:
            r -= INCREMENT
        print key

print r
