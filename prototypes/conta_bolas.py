#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import cv2
import numpy as np

# key pressed (used to escape screen and close)
key = 0

# ler stream da webcam
captura = cv2.VideoCapture(0)

while key != 27 and key != 1048603: # tecla ESC no notebook e no desktop
    _, im = captura.read()

    # BGR
    cor_alvo_min = np.array([0,0,80])
    cor_alvo_max = np.array([30,30,255])
    
    # obter somente a componente vermelha da imagem
    mascara = cv2.inRange(im, cor_alvo_min, cor_alvo_max)
    
    # identifica os contornos dos objetos vermelhos encontrados
    contornos, hierarquia = cv2.findContours(mascara,
                                             cv2.RETR_TREE,
                                             cv2.CHAIN_APPROX_SIMPLE)

    # quantidade de objetos
    objetos = 0

    # retangulos
    for contorno in contornos:
        if cv2.contourArea(contorno) > 200: # considera apenas objetos grandes
            objetos += 1
            ret_x, ret_y, ret_w, ret_h = cv2.boundingRect(contorno)
            cv2.rectangle(im, (ret_x,ret_y), 
                              (ret_x+ret_w, 
                               ret_y+ret_h),
                              (0,255,255),2)

    # mostra contagem
    cv2.putText(im,
                '%02d' % objetos,
                (500,70),
                cv2.FONT_HERSHEY_TRIPLEX, 3, (255,0,0))

    #linha verde
    altura_linha = 170
    cv2.line(im,
             (0,altura_linha), (800,altura_linha),
             (0,255,0), # cor verde
             thickness=3)

    cv2.imshow('Resultado', im)
    # cv2.imshow('Resultado', resultado)
    
    key = cv2.waitKey(10)
    # if key != -1: print key


