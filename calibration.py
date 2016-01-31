#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time
import Tkinter as tk

class Calibrator(object):

    def __init__(self):
        self.blue_min = 0
        self.green_min = 0
        self.red_min = 0
        self.blue_max = 0
        self.green_max = 0
        self.red_max = 0
   
    def set_blue_min(self, val):
        self.blue_min = val

    def set_green_min(self, val):
        self.green_min = val

    def set_red_min(self, val):
        self.red_min = val
    
    def set_blue_max(self, val):
        self.blue_max = val

    def set_green_max(self, val):
        self.green_max = val

    def set_red_max(self, val):
        self.red_max = val

    def calibrate(self, im):
        print 'calibrating'
        root = tk.Tk()
    
        blue_min_scale = tk.Scale(
                                  master=root,
                                  to=255,
                                  command=self.set_blue_min)

        green_min_scale = tk.Scale(
                                   master=root,
                                   to=255,
                                   command=self.set_green_min)

        red_min_scale = tk.Scale(
                                   master=root,
                                   to=255,
                                   command=self.set_red_min)

        red_min_scale.pack(side=tk.LEFT)
        green_min_scale.pack(side=tk.LEFT)
        blue_min_scale.pack(side=tk.LEFT)
    
        blue_max_scale = tk.Scale(
                                  master=root,
                                  to=255,
                                  command=self.set_blue_max)

        green_max_scale = tk.Scale(
                                   master=root,
                                   to=255,
                                   command=self.set_green_max)

        red_max_scale = tk.Scale(
                                   master=root,
                                   to=255,
                                   command=self.set_red_max)

        red_max_scale.pack(side=tk.LEFT)
        green_max_scale.pack(side=tk.LEFT)
        blue_max_scale.pack(side=tk.LEFT)
    
        root.mainloop()
    
        colors = {}
        min_color = (self.blue_min,self.green_min,self.red_min)
        max_color = (self.blue_max,self.green_max,self.red_max)
        colors['min'] = min_color
        colors['max'] = max_color
    
        return colors
