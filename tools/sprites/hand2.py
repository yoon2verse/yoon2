"""Groom traced from the reference: 32 x 63, head 34 rows / body 29 rows."""
import hand
from hand import PAL, put, sym_fill, outline, overlay, stamp, mirror_rows, overlay_hair
hand.H = H = 63
W = hand.W
AX = 31


def blank():
    return [['.'] * W for _ in range(H)]


hand.blank = blank


def from_rows(rows, y0=0):
    g = blank()
    for dy, r in enumerate(rows):
        for x, c in enumerate(r):
            put(g, x, y0 + dy, c)
    return g


FACE_HW = {y: 11 for y in range(12, 31)}
FACE_HW.update({31: 10, 32: 9, 33: 7})


def base_head():
    g = blank()
    sym_fill(g, FACE_HW, 'S')
    for y in range(24, 30):           # ears
        for x in (3, 4):
            put(g, x, y, 'S')
            put(g, AX - x, y, 'S')
    outline(g, 'S', 'k')
    for y in (31, 32, 33):
        w = FACE_HW[y]
        put(g, 16 - w, y, 's')
        put(g, 15 + w, y, 's')
    for y in range(25, 29):
        put(g, 4, y, 's')
        put(g, AX - 4, y, 's')
    return g


def face():
    g = blank()
    eye = ['.EE.', 'EWEE', 'EEEE', 'EIIE', '.EE.']
    stamp(g, 7, 24, eye)
    stamp(g, AX - 10, 24, eye)
    stamp(g, 5, 29, ['.BB.', 'BBBB'], mirror=True)
    stamp(g, 14, 30, ['M..M', '.MM.'])
    return g


HAIR_OUTER = {0: 2, 1: 4, 2: 7, 3: 9, 4: 11, 5: 13, 6: 14}
HAIR_OUTER.update({y: 15 for y in range(7, 23)})
HAIR_OUTER.update({23: 14, 24: 14, 25: 14, 26: 14, 27: 14, 28: 14, 29: 13})
# first visible face row per column (traced from the reference)
BANGS = {5: 24, 6: 23, 7: 22, 8: 22, 9: 20, 10: 20, 11: 21, 12: 21, 13: 20, 14: 16, 15: 15,
         16: 14, 17: 14, 18: 14, 19: 14, 20: 14, 21: 15, 22: 15, 23: 18, 24: 19, 25: 22, 26: 24}
EAR_ROWS = range(24, 30)


def hair():
    from refhair import underlay, hair_grid
    _, lum = underlay((22, 22, 96, 176), 31, shift=1)

    def allow(x, y):
        if y >= 31:
            return False
        if y >= 22 and 5 <= x <= 26:      # below the bangs only side hair, never eyes/brows
            return False
        if 3 <= x <= 4 or 27 <= x <= 28:  # ears
            return not (24 <= y <= 29)
        return True
    g = hair_grid(lum, allow, W, H, light=52)
    # tidy, symmetric side hair: sideburns down to the ears, neat rounded ends
    side = {y: (1, 4) for y in range(14, 24)}
    side.update({y: (1, 2) for y in range(24, 30)})
    side.update({30: (2, 2)})
    for y in range(12, 33):
        lo, hi = side.get(y, (99, -1))
        for x in range(0, 5):
            for xx in (x, AX - x):
                if y < 14:
                    continue
                if lo <= x <= hi:
                    if g[y][xx] == '.':
                        g[y][xx] = 'H'
                else:
                    g[y][xx] = '.'
    outline(g, 'Hhj', 'O')
    return g


BODY = mirror_rows([
    '......OOOOOOtCOO',
    '....OOTTTTTtCOOO',
    '...OtTTTTTTTtCOC',
    '..OtTTTTTTTTTtCC',
    '..OtTTTTTTTTTtCC',
    '.OtTTOTTTTTTTTtC',
    '.OtTTOTTTTTTTTtC',
    '.OtTTOTTTTTTTTTt',
    '.OtTTOTTTTTTTTTt',
    '.OtTTOTTTTTTTTTT',
    '.OtTTOTTTTTTTTTT',
    '.OtTTOTTTTTTTTTT',
    '.OtTTOTTTTTTTTTT',
    '.OCCCOTTTTTTTTTT',
    '.kSSSkTTTTTTTTTT',
    '.kSSSkTTTTTTTTTT',
    '..kkk.OTTTTTTTTT',
    '......OTTTTTTTTT',
    '......OOOOOOOOOO',
    '.......OtTTTTTTO',
    '.......OtTTTTTTO',
    '.......OtTTTTTTO',
    '.......OtTTTTTTO',
    '.......OtTTTTTTO',
    '.......OtTTTTTTO',
    '.......OtTTTTTTO',
    '......OFFFFFFFFO',
    '......OFFFFFFFFO',
    '.......OOOOOOOO.',
])


def groom():
    g = base_head()
    overlay(g, face())
    overlay_hair(g, hair())
    # brows only where the bangs leave skin showing
    for x in (7, 8, 9, 22, 23, 24):
        if g[22][x] == 'S':
            g[22][x] = 'h'
    # keep the two side locks symmetric in length: nothing below row 30
    overlay(g, from_rows(BODY, 34))
    stamp(g, 19, 38, ['RR', 'Rg'])
    return g


def save(g, name):
    from PIL import Image
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            if g[y][x] != '.':
                im.putpixel((x, y), PAL[g[y][x]] + (255,))
    im.save(name)


if __name__ == '__main__':
    save(groom(), 'hand2_groom.png')
