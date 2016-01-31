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
    
    def set_blue_min(self, val):
        self.blue_min = val

    def set_green_min(self, val):
        self.green_min = val

    def set_red_min(self, val):
        self.red_min = val
    
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
    
        blue_max_scale = tk.Scale(master=root, to=255)
        green_max_scale = tk.Scale(master=root, to=255)
        red_max_scale = tk.Scale(master=root, to=255)
        red_max_scale.pack(side=tk.LEFT)
        green_max_scale.pack(side=tk.LEFT)
        blue_max_scale.pack(side=tk.LEFT)
    
        root.mainloop()
    
        colors = {}
        min_color = (self.blue_min,self.green_min,self.red_min)
        max_color = (255,255,255)
        colors['min'] = min_color
        colors['max'] = max_color
    
        return colors
