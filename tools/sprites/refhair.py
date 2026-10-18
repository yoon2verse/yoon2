"""Hair mask + highlights traced directly from the reference image."""
from PIL import Image
import numpy as np


def underlay(box, width, shift=0):
    im = Image.open('ref_couple.jpg').convert('RGB').crop(box)
    h = round(im.height * width / im.width)
    a = np.asarray(im.resize((width, h), Image.LANCZOS)).astype(float)
    lum = a @ np.array([0.3, 0.59, 0.11])
    if shift:
        lum = np.pad(lum, ((0, 0), (shift, 0)), constant_values=255)
        a = np.pad(a, ((0, 0), (shift, 0), (0, 0)), constant_values=255)
    return a, lum


def hair_grid(lum, allow, W, H, dark=110, light=72):
    """allow(x, y) -> may this cell be hair. Returns rows of 'H'/'h'/'.'."""
    g = [['.'] * W for _ in range(H)]
    for y in range(min(H, lum.shape[0])):
        for x in range(min(W, lum.shape[1])):
            if lum[y, x] < dark and allow(x, y):
                g[y][x] = 'h' if lum[y, x] > light else 'H'
    # fill pinholes, drop specks
    for _ in range(2):
        for y in range(1, H - 1):
            for x in range(1, W - 1):
                n = sum(g[y + dy][x + dx] != '.' for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if g[y][x] == '.' and n >= 3 and allow(x, y):
                    g[y][x] = 'H'
                elif g[y][x] != '.' and n <= 1:
                    g[y][x] = '.'
    return g
