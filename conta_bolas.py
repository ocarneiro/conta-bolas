#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import cv2
import numpy as np

# key pressed (used to escape screen and close)
key = 0

# ler stream da webcam
captura = cv2.VideoCapture(0)

while key != 27 and key != 1048603:
    _, im = captura.read()

    # BGR
    cor_alvo_min = np.array([0,0,80])
    cor_alvo_max = np.array([30,30,255])
    
    # obter somente a componente vermelha da imagem
    # ref: https://pythonprogramming.net/color-filter-python-opencv-tutorial/
    mascara = cv2.inRange(im, cor_alvo_min, cor_alvo_max)
    
    # identifica os contornos dos objetos vermelhos encontrados
    contornos, hierarquia = cv2.findContours(mascara,
                                             cv2.RETR_TREE,
                                             cv2.CHAIN_APPROX_SIMPLE)

    # quantidade de objetos
    objetos = 0

    # retangulos: 
    # http://stackoverflow.com/questions/16538774/
    #     dealing-with-contours-and-bounding-rectangle-in-opencv-2-4-python-2-7
    for contorno in contornos:
        if cv2.contourArea(contorno) > 200: # considera apenas objetos grandes
            objetos += 1
            ret_x, ret_y, ret_w, ret_h = cv2.boundingRect(contorno)
            cv2.rectangle(im, (ret_x,ret_y), 
                              (ret_x+ret_w, 
                               ret_y+ret_h),
                              (0,255,255),2)

    # print objetos
    cv2.putText(im,
                u'Encontrei %d objetos' % objetos,
                (10,450),
                cv2.FONT_HERSHEY_TRIPLEX, 1, (255,255,255))

    cv2.imshow('Resultado', im)
    # cv2.imshow('Resultado', resultado)
    
    key = cv2.waitKey(10)
    # if key != -1: print key


