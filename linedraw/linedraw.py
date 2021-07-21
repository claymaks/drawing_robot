from random import *
import math
import argparse

from PIL import Image, ImageDraw, ImageOps

from linedraw.filters import *
from linedraw.strokesort import *
from linedraw import perlin
from linedraw.util import *

no_cv = False
export_path = "output/out.svg"
draw_contours = True
draw_hatch = True
show_bitmap = False
resolution = 1024
hatch_size = 16
contour_simplify = 2

try:
    import numpy as np
    import cv2
except:
    print("Cannot import numpy/openCV. Switching to NO_CV mode.")
    no_cv = True


def find_edges(IM):
    if no_cv:
        # appmask(IM,[F_Blur])
        appmask(IM, [F_SobelX, F_SobelY])
    else:
        im = np.array(IM)
        im = cv2.GaussianBlur(im, (3, 3), 0)
        im = cv2.Canny(im, 100, 200)
        IM = Image.fromarray(im)
    return IM.point(lambda p: p > 128 and 255)


def getdots(IM):
    PX = IM.load()
    dots = []
    w, h = IM.size
    for y in range(h - 1):
        row = []
        for x in range(1, w):
            if PX[x, y] == 255:
                if len(row) > 0:
                    if x - row[-1][0] == row[-1][-1] + 1:
                        row[-1] = (row[-1][0], row[-1][-1] + 1)
                    else:
                        row.append((x, 0))
                else:
                    row.append((x, 0))
        dots.append(row)
    return dots


def connectdots(dots):
    contours = []
    for y in range(len(dots)):
        for x, v in dots[y]:
            if v > -1:
                if y == 0:
                    contours.append([(x, y)])
                else:
                    closest = -1
                    cdist = 100
                    for x0, v0 in dots[y - 1]:
                        if abs(x0 - x) < cdist:
                            cdist = abs(x0 - x)
                            closest = x0

                    if cdist > 3:
                        contours.append([(x, y)])
                    else:
                        found = 0
                        for i in range(len(contours)):
                            if contours[i][-1] == (closest, y - 1):
                                contours[i].append((x, y,))
                                found = 1
                                break
                        if found == 0:
                            contours.append([(x, y)])
        for c in contours:
            if c[-1][1] < y - 1 and len(c) < 4:
                contours.remove(c)
    return contours


def getcontours(IM, sc=2):
    IM = find_edges(IM)
    IM1 = IM.copy()
    IM2 = IM.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
    dots1 = getdots(IM1)
    contours1 = connectdots(dots1)
    dots2 = getdots(IM2)
    contours2 = connectdots(dots2)

    for i in range(len(contours2)):
        contours2[i] = [(c[1], c[0]) for c in contours2[i]]
    contours = contours1 + contours2

    for i in range(len(contours)):
        for j in range(len(contours)):
            if len(contours[i]) > 0 and len(contours[j]) > 0:
                if distsum(contours[j][0], contours[i][-1]) < 8:
                    contours[i] = contours[i] + contours[j]
                    contours[j] = []

    for i in range(len(contours)):
        contours[i] = [contours[i][j] for j in range(0, len(contours[i]), 8)]

    contours = [c for c in contours if len(c) > 1]

    for i in range(0, len(contours)):
        contours[i] = [(v[0] * sc, v[1] * sc) for v in contours[i]]

    for i in range(0, len(contours)):
        for j in range(0, len(contours[i])):
            contours[i][j] = int(contours[i][j][0] + 10 * perlin.noise(i * 0.5, j * 0.1, 1)), int(
                contours[i][j][1] + 10 * perlin.noise(i * 0.5, j * 0.1, 2))

    return contours


def _sketch(img):
    IM = Image.fromarray(img)
    w, h = IM.size

    IM = IM.convert("L")
    IM = ImageOps.autocontrast(IM, 10)

    lines = []
    if draw_contours:
        lines += getcontours(IM, 2)

    lines = sortlines(lines)

    return lines
