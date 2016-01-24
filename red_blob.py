import cv2
import numpy as np

im = cv2.imread('3bolas.jpg', cv2.IMREAD_COLOR)
cv2.imshow('Original', im)

# BGR
cor_alvo_min = np.array([0,0,80])
cor_alvo_max = np.array([30,30,255])

mascara = cv2.inRange(im, cor_alvo_min, cor_alvo_max)
resultado = cv2.bitwise_and(im, im, mask=mascara)
# converte imagem para fundo branco e mascara em preto
inv_masc = 255 - mascara

params = cv2.SimpleBlobDetector_Params()
params.filterByConvexity = False
params.filterByInertia = False

detector = cv2.SimpleBlobDetector(params)

keypoints = detector.detect(inv_masc)
im_with_keypoints = cv2.drawKeypoints(inv_masc, keypoints, np.array([]), (0,255,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow("Keypoints", im_with_keypoints)

key = 0
while key != 27 and key != 1048603:
    key = cv2.waitKey(10)
    # if key != -1: print key


