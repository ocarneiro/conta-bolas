import cv2
import numpy as np

key = 0
captura = cv2.VideoCapture(0)

while key != 27 and key != 1048603:
    _, im = captura.read()

    # BGR
    cor_alvo_min = np.array([0,0,80])
    cor_alvo_max = np.array([30,30,255])
    
    mascara = cv2.inRange(im, cor_alvo_min, cor_alvo_max)
    contornos, hierarquia = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # TODO substituir por retângulos
    # http://stackoverflow.com/questions/16265627/blob-detection-with-python-opencv
    cv2.drawContours(im, contornos, -1, (0,255,255), 3)
    
    cv2.imshow('Tratado', im)
    # cv2.imshow('Resultado', resultado)
    
    key = cv2.waitKey(10)
    # if key != -1: print key


