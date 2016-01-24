import cv2
import numpy as np

im = cv2.imread('3bolas.jpg', cv2.IMREAD_COLOR)

# BGR
cor_alvo_min = np.array([0,0,80])
cor_alvo_max = np.array([30,30,255])

mascara = cv2.inRange(im, cor_alvo_min, cor_alvo_max)
contornos, hierarquia = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(im, contornos, -1, (0,0,0), 3)

cv2.imshow('Original', im)
# cv2.imshow('Resultado', resultado)

key = 0
while key != 27 and key != 1048603:
    key = cv2.waitKey(10)
    # if key != -1: print key


