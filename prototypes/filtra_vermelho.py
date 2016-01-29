import cv2
import numpy as np

im = cv2.imread('3bolas.jpg', cv2.IMREAD_COLOR)
cv2.imshow('Original', im)

# BGR
cor_alvo_min = np.array([0,0,80])
cor_alvo_max = np.array([30,30,255])

mascara = cv2.inRange(im, cor_alvo_min, cor_alvo_max)
resultado = cv2.bitwise_and(im, im, mask=mascara)

cv2.imshow('Resultado', resultado)

key = 0
while key != 27:
    key = cv2.waitKey(10)


