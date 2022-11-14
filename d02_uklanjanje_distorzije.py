import cv2
import numpy as np
from copy import deepcopy

import lib.pg_transform as pgt

# Unete tačke
points = []

# Pokretanje prozora za unos
def mouseCallback(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img1_copy,(x,y),15,(0,0,255),-1)
        points.append(np.array([x,y,1]))

img1 = cv2.imread("./prilozi/d01_original.jpeg")
img1_copy = deepcopy(img1)
cv2.namedWindow("otklanjanje_distorzije")
cv2.setMouseCallback("otklanjanje_distorzije", mouseCallback)

running = True
while(running):
    cv2.imshow("otklanjanje_distorzije", img1_copy)
    k = cv2.waitKey(20) & 0xFF
    if k == 13:
        running = False


# Izlaz iz programa ako nema dovoljno tačaka
if len(points) < 4:
    exit()

# Uzimamo samo prve 4 unete tačke
points1 = points[:4]

img_height = img1.shape[0]
img_width = img1.shape[1]

# Taček u koje slikamo odabrane tačke
points2 = np.array([[0, 0, 1],
                    [img_width, 0, 1],
                    [0, img_height, 1],
                    [img_width, img_height, 1]])

# Računanje matrice transofrmacije
f = pgt.dlt(points1, points2)

# Uklanjanje distorzije
img2 = cv2.warpPerspective(img1, f, (img_width, img_height), flags = cv2.INTER_LINEAR)

# Prikaz rezultata
cv2.imshow("Rezultat", img2)
cv2.waitKey()