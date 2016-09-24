#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import sys   # used to get command line parameter

WINDOW_NAME = "ocarneiro/conta-bolas"
DEBUG_WINDOW = "DEBUG"

MARGIN_LEFT = 10
MARGIN_TOP = 400
FILLED = -1
INCREMENT = 2
SCALE = 1
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)
MIN_VALUE = 0
MAX_VALUE = 255
DOT_SIZE = 20

PARAM_NAMES = ("hue_min", "sat_min", "val_min",
               "hue_max", "sat_max", "val_max")
INIT_VALUES = (94, 86, 52, 124, 255, 169)

PRESET_BLUE = (94, 86, 52, 124, 255, 169)  # for blue ball
PRESET_RED = (114, 102, 124, 185, 255, 255)  # for red ball
PRESET_YELLOW = (18, 102, 122, 75, 193, 255)  # for yellow ball
PRESET_BANK = (PRESET_BLUE, PRESET_RED, PRESET_YELLOW)


class Slider(object):
    """Control containing its value, presentation color,
        position (integer indicating a slot on the screen),
        plus and minus keys (keys that add or subtract from value"""

    def __init__(self, init_value, color, position, plus_key, minus_key):
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
    """Main class, responsible for the whole logic and setup"""

    def __init__(self, capture, threshold):
        self.mirror_mode = True
        self.debug_mode = False
        self.window_name = WINDOW_NAME
        self.sliders = {
                "hue_min": Slider(INIT_VALUES[0], GREEN, 0, 113, 97),
                "sat_min": Slider(INIT_VALUES[1], RED, 1, 119, 115),
                "val_min": Slider(INIT_VALUES[2], WHITE, 2, 101, 100),
                "hue_max": Slider(INIT_VALUES[3], GREEN, 3, 114, 102),
                "sat_max": Slider(INIT_VALUES[4], RED, 4, 116, 103),
                "val_max": Slider(INIT_VALUES[5], WHITE, 5, 121, 104)
                 }
        self.capture = capture
        self.threshold = threshold
        self.get_feed()
        self.init_keys()
        self.preset_applied = 0

    def apply_preset(self, preset):
        """Set parameters as defined in preset list or tuple"""
        for num, name in enumerate(PARAM_NAMES):
            self.sliders[name].value = preset[num]

    def toggle_preset(self):
        self.preset_applied += 1
        if self.preset_applied >= len(PRESET_BANK):
            self.preset_applied = 0
        self.apply_preset(PRESET_BANK[self.preset_applied])

    def apply_red(self):
        self.apply_preset(PRESET_RED)

    def apply_blue(self):
        self.apply_preset(PRESET_BLUE)

    def apply_yellow(self):
        self.apply_preset(PRESET_YELLOW)

    def init_keys(self):
        """Sets functions for keys pressed"""
        self.key_map = {}
        # uses keys defined on slider initialization
        for _, slider in self.sliders.iteritems():
            self.key_map[slider.minus_key] = slider.decrease
            self.key_map[slider.plus_key] = slider.increase
        # set function key F1 for debug mode
        self.key_map[65470] = self.toggle_debug_mode  # F1
        # set presets for F2, F3 and F4
        self.key_map[65471] = self.apply_red
        self.key_map[65472] = self.apply_blue
        self.key_map[65473] = self.apply_yellow
        # set toggle preset to F5
        self.key_map[65474] = self.toggle_preset

    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode
        if not self.debug_mode:
            cv2.destroyWindow(DEBUG_WINDOW)

    def get_feed(self):
        _, self.image = self.capture.read()
        if self.mirror_mode:
            cv2.flip(self.image, 1, self.image)

    def mask_image(self):
        """Converts image to HSV mode and
        filters color using values defined in sliders"""

        hsv_im = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        h = self.sliders['hue_min'].value
        s = self.sliders['sat_min'].value
        v = self.sliders['val_min'].value
        min_target_color = np.array([h, s, v])
        h = self.sliders['hue_max'].value
        s = self.sliders['sat_max'].value
        v = self.sliders['val_max'].value
        max_target_color = np.array([h, s, v])
        self.mask = cv2.inRange(hsv_im,
                                min_target_color,
                                max_target_color)

    def draw_contours(self):
        """"""
        # contours all the objects found
        # (findContours changes the source image,
        #  hence copy)
        contours, _ = cv2.findContours(self.mask.copy(),
                                       cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)
        # rectangles
        for contour in contours:
            size = cv2.contourArea(contour)
            if size > self.threshold:  # only larger objects
                ret_x, ret_y, ret_w, ret_h = cv2.boundingRect(contour)
                cv2.rectangle(self.display, (ret_x, ret_y),
                              (ret_x+ret_w,
                               ret_y+ret_h),
                              (0, 255, 255), 2)

    def play(self):
        key = 0
        j = self
        while key != 27 and key != 1048603:
            j.get_feed()
            self.display = self.image  # TODO copy to add interaction later

            key = cv2.waitKey(10)
            if key >= 0:
                j.act_on_key(key)

            self.mask_image()
            self.draw_contours()

            cv2.imshow(self.window_name, self.display)

            if self.debug_mode:
                self.debug_image = cv2.cvtColor(self.mask, cv2.COLOR_GRAY2BGR)
                j.draw_sliders(self.debug_image)
                cv2.imshow(DEBUG_WINDOW, self.debug_image)

    def act_on_key(self, key):
        if key in self.key_map:
            self.key_map[key]()
        else:
            print key

    def draw_slider(self, slider, image):
        cv2.circle(image,
                   (slider.position, MARGIN_TOP - slider.value * SCALE),
                   DOT_SIZE/2, slider.color, FILLED)

    def draw_sliders(self, image):
        for _, slider in self.sliders.iteritems():
            self.draw_slider(slider, image)


def print_help():
    print "Usage: "
    print "python conta_bolas.py CAMERA RES_X RES_Y THRES"
    print "CAMERA = index of webcam to be used"
    print "RES_X = resolution width"
    print "RES_Y = resolution height"
    print "THRES = threshold for object detection"

# default camera = 0
camera = 0
threshold = 300

# setup webcam
if len(sys.argv) > 1:
    if 'h' in sys.argv[1]:
        print_help()
    else:
        camera = int(sys.argv[1])

capture = cv2.VideoCapture(camera)
if len(sys.argv) > 2:
    # cv2.VideoCapture.set(CV_CAP_PROP_FRAME_WIDTH, int(sys,argv[2]))
    capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, int(sys.argv[2]))
    capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, int(sys.argv[3]))
    threshold = int(sys.argv[4])

j = Juggling(capture, threshold)
j.play()

# prints values last used for calibration
for item in PARAM_NAMES:
    print "%s," % j.sliders[item].value,
