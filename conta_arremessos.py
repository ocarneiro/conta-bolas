#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import cv2
import numpy as np

# key pressed (used to escape screen and close)
key = 0

# ler stream da webcam
captura = cv2.VideoCapture(0)

# quantidade de arremessos
arremessos = 0

#linha verde
altura_linha = 170

visivel = False # a bola está na tela?
abaixo = False  # abaixo da linha?
acima = False   # ou acima dela?

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

    # desenha linha
    cv2.line(im,
             (0,altura_linha), (800,altura_linha),
             (0,255,0), # cor verde
             thickness=3)

    # retangulos
    for contorno in contornos:
        if cv2.contourArea(contorno) > 200: # considera apenas objetos grandes
            visivel = True
            ret_x, ret_y, ret_w, ret_h = cv2.boundingRect(contorno)
            cv2.rectangle(im, (ret_x,ret_y), 
                              (ret_x+ret_w, 
                               ret_y+ret_h),
                              (0,255,255),2)

    # onde está a bola?
    if visivel:
        if ret_y < altura_linha:
            acima = True
            abaixo = False
        else:
            abaixo = True

    if acima and abaixo:
        arremessos += 1
        abaixo = False
        acima = False

    # mostra contagem
    cv2.putText(im,
                '%02d' % arremessos,
                (500,70),
                cv2.FONT_HERSHEY_TRIPLEX, 3, (255,0,0))

    cv2.imshow('Resultado', im)
    # cv2.imshow('Resultado', resultado)
    
    key = cv2.waitKey(10)
    # if key != -1: print key


