import cv2
import numpy as np

im = cv2.imread('vermelho.jpg', cv2.IMREAD_COLOR)
cv2.imshow('Original', im)

hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

cor_alvo_min = np.array([30,150,50])
cor_alvo_max = np.array([255,255,180])

mascara = cv2.inRange(hsv, cor_alvo_min, cor_alvo_max)
resultado = cv2.bitwise_and(im, im, mask=mascara)

cv2.imshow('Resultado', resultado)

key = 0
while key != 27:
    key = cv2.waitKey(10)


