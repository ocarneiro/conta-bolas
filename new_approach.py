#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import cv2

mirror_mode = True

WINDOW_NAME = "ocarneiro/conta-bolas"
MARGIN_LEFT = 10
MARGIN_TOP = 10
FILLED = -1
INCREMENT = 2
SCALE = INCREMENT
RED = (0,0,255)
MIN_VALUE = 0
MAX_VALUE = 25

class ColorValue(object):
    def __init__(self, init_value):
        self.value = init_value

    def decrease(self, amount):
        self.value -= amount
        if self.value < MIN_VALUE:
            self.value = MIN_VALUE 

    def increase(self, amount):
        self.value += amount
        if self.value > MAX_VALUE:
            self.value = MAX_VALUE 

    def __str__(self):
        return str(self.value)

class Juggling(object):

    def __init__(self, capture):
        self.mirror_mode = True
        self.window_name = WINDOW_NAME
        self.r = ColorValue(20)
        self.capture = capture
        self.get_feed()

    def get_feed(self):
        _, self.image = self.capture.read()
        if self.mirror_mode:
            cv2.flip(self.image, 1, self.image)

    def show(self):
        cv2.imshow(self.window_name, self.image)

    def act_on_key(self, key):
        if key == 113:
            self.r.decrease(INCREMENT)
        if key == 97:
            self.r.increase(INCREMENT)
#        print key


# setup webcam
capture = cv2.VideoCapture(0)

j = Juggling(capture)

key = 0

while key != 27 and key != 1048603:
    j.get_feed()
    cv2.circle(j.image, (MARGIN_LEFT, MARGIN_TOP + j.r.value * SCALE), 10, RED, FILLED)
    j.show()
    key = cv2.waitKey(10)
    if key >= 0:
        j.act_on_key(key)
print j.r
