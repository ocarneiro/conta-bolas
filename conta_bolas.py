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

    # contagem de objetos
#    objetos = 0
#    while contornos:
#        objetos += 1
#        contornos = contornos.h_next()
#
#    # escreve (TODO na imagem) a quantidade de objetos encontrada
#    print len(objetos)
#
    print(len(contornos))
    # TODO substituir por retângulos
    # http://stackoverflow.com/questions/16265627/blob-detection-with-python-opencv
    # cv2.drawContours(im, contornos, -1, (0,255,255), 3)

    # retangulos: http://stackoverflow.com/questions/16538774/dealing-with-contours-and-bounding-rectangle-in-opencv-2-4-python-2-7
    for contorno in contornos:
        if cv2.contourArea(contorno) > 30:
            ret_x, ret_y, ret_w, ret_h = cv2.boundingRect(contorno)
            cv2.rectangle(im, (ret_x,ret_y), 
                              (ret_x+ret_w, 
                               ret_y+ret_h),
                              (0,255,0),2)
    
    cv2.imshow('Resultado', im)
    # cv2.imshow('Resultado', resultado)
    
    key = cv2.waitKey(10)
    # if key != -1: print key


