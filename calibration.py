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
        self.blue_min = int(val)

    def set_green_min(self, val):
        self.green_min = int(val)

    def set_red_min(self, val):
        self.red_min = int(val)
    
    def set_blue_max(self, val):
        self.blue_max = int(val)

    def set_green_max(self, val):
        self.green_max = int(val)

    def set_red_max(self, val):
        self.red_max = int(val)

    def calibrate(self, im, colors):
        root = tk.Tk()
        bmin, gmin, rmin = colors.colors['min']
        min_target_color = np.array([bmin,gmin,rmin])
        bmax, gmax, rmax = colors.colors['max']
    
        blue_min_scale = tk.Scale(
                                  master=root,
                                  to=255,
                                  command=self.set_blue_min,
                                  label='Bmin')
        blue_min_scale.set(bmin)

        green_min_scale = tk.Scale(
                                   master=root,
                                   to=255,
                                   command=self.set_green_min,
                                   label='Gmin')
        green_min_scale.set(gmin)

        red_min_scale = tk.Scale(
                                   master=root,
                                   to=255,
                                   command=self.set_red_min,
                                   label='Rmin')
        red_min_scale.set(rmin)

        red_min_scale.pack(side=tk.LEFT)
        green_min_scale.pack(side=tk.LEFT)
        blue_min_scale.pack(side=tk.LEFT)
    
        blue_max_scale = tk.Scale(
                                  master=root,
                                  to=255,
                                  command=self.set_blue_max,
                                  label='Bmax')
        blue_max_scale.set(bmax)

        green_max_scale = tk.Scale(
                                   master=root,
                                   to=255,
                                   command=self.set_green_max,
                                   label='Gmax')
        green_max_scale.set(gmax)

        red_max_scale = tk.Scale(
                                   master=root,
                                   to=255,
                                   command=self.set_red_max,
                                   label='Rmax')
        red_max_scale.set(rmax)

        red_max_scale.pack(side=tk.LEFT)
        green_max_scale.pack(side=tk.LEFT)
        blue_max_scale.pack(side=tk.LEFT)
    
        root.mainloop()
    
        colors = Colors(
                        self.blue_min,
                        self.green_min,
                        self.red_min,
                        self.blue_max,
                        self.green_max,
                        self.red_max)
        return colors

class Colors(object):

    def __init__(self,b,g,r,bm,gm,rm):
        self.colors = {}
        min_color = (b,g,r)
        max_color = (bm,gm,rm)
        self.colors['min'] = min_color
        self.colors['max'] = max_color
