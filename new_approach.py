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
WHITE = (255,255,255)
MIN_VALUE = 0
MAX_VALUE = 25
DOT_SIZE = 20 

class Slider(object):
    def __init__(self, init_value, color, position, minus_key, plus_key):
        self.value = init_value
        self.color = color
        self.position = MARGIN_LEFT + position * DOT_SIZE
        self.minus_key = minus_key
        self.plus_key = plus_key

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
        self.sliders = {
                "hue_min": Slider(50, GREEN, 0, 113, 97),
                "sat_min": Slider(50, RED, 1, 119, 115),
                "val_min": Slider(50, WHITE, 2, 101, 100),
                "hue_max": Slider(50, GREEN, 3, 114, 102),
                "sat_max": Slider(50, RED, 4, 116, 103),
                "val_max": Slider(50, WHITE, 5, 121, 104)
                 }
        self.capture = capture
        self.get_feed()
        self.key_map = {}
        for _, slider in self.sliders.iteritems():
            self.key_map[slider.minus_key] = slider.decrease
            self.key_map[slider.plus_key] = slider.increase

    def get_feed(self):
        _, self.image = self.capture.read()
        if self.mirror_mode:
            cv2.flip(self.image, 1, self.image)

    def play(self):
        cv2.imshow(self.window_name, self.image)

    def act_on_key(self, key):
        if key in self.key_map:
            self.key_map[key]()
        else:
            print key

    def draw_slider(self, slider):
        cv2.circle(self.image, 
                   (slider.position, MARGIN_TOP + slider.value * SCALE), 
                   DOT_SIZE/2, slider.color, FILLED)

    def draw_sliders(self):
        for _, slider in self.sliders.iteritems():
            self.draw_slider(slider)


# setup webcam
capture = cv2.VideoCapture(0)
j = Juggling(capture)
key = 0

while key != 27 and key != 1048603:
    j.get_feed()
    j.draw_sliders()
    j.play()
    key = cv2.waitKey(10)
    if key >= 0:
        j.act_on_key(key)
print j.r
