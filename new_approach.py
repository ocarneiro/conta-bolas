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
GREEN = (0,255,0)
BLUE = (255,0,0)
MIN_VALUE = 0
MAX_VALUE = 25
DOT_SIZE = 20 

class ColorValue(object):
    def __init__(self, init_value, color):
        self.value = init_value
        self.color = color

    def decrease(self):
        self.value -= INCREMENT
        if self.value < MIN_VALUE:
            self.value = MIN_VALUE 

    def increase(self):
        self.value += INCREMENT
        if self.value > MAX_VALUE:
            self.value = MAX_VALUE 

    def __str__(self):
        return str(self.value)

class Juggling(object):

    def __init__(self, capture):
        self.mirror_mode = True
        self.window_name = WINDOW_NAME
        self.r = ColorValue(20, RED)
        self.g = ColorValue(20, GREEN)
        self.b = ColorValue(20, BLUE)
        self.capture = capture
        self.get_feed()
        self.key_map = {
            113: self.r.decrease,
            97:  self.r.increase,
            119: self.g.decrease,
            115: self.g.increase,
            101: self.b.decrease,
            100: self.b.increase
        }

    def get_feed(self):
        _, self.image = self.capture.read()
        if self.mirror_mode:
            cv2.flip(self.image, 1, self.image)

    def show(self):
        cv2.imshow(self.window_name, self.image)

    def act_on_key(self, key):
        if key in self.key_map:
            self.key_map[key]()

    def draw_sliders(self):
        j = self
        cv2.circle(j.image, 
                   (MARGIN_LEFT, MARGIN_TOP + j.r.value * SCALE), 
                   DOT_SIZE/2, j.r.color, FILLED)
        cv2.circle(j.image, 
                   (MARGIN_LEFT + DOT_SIZE, MARGIN_TOP + j.g.value * SCALE), 
                   DOT_SIZE/2, j.g.color, FILLED)
        cv2.circle(j.image, 
                   (MARGIN_LEFT + 2*DOT_SIZE, MARGIN_TOP + j.b.value * SCALE), 
                   DOT_SIZE/2, j.b.color, FILLED)

# setup webcam
capture = cv2.VideoCapture(0)
j = Juggling(capture)
key = 0

while key != 27 and key != 1048603:
    j.get_feed()
    j.draw_sliders()
    j.show()
    key = cv2.waitKey(10)
    if key >= 0:
        j.act_on_key(key)
print j.r