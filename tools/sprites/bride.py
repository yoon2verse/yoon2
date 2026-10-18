"""Bride traced from the reference: 42 x 64, body axis between x=18 and x=19."""
from PIL import Image
from hand import PAL
from refhair import underlay, hair_grid

W, H = 42, 64
AX = 37                      # mirror x -> AX - x (axis 18.5)
SHIFT = -2                   # underlay x -> canvas x


def blank():
    return [['.'] * W for _ in range(H)]


def put(g, x, y, c):
    if 0 <= x < W and 0 <= y < H and c != '.':
        g[y][x] = c


def outline(g, fill, ch, only_on='.'):
    pts = []
    for y in range(H):
        for x in range(W):
            if g[y][x] not in only_on:
                continue
            if any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] in fill
                   for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                pts.append((x, y))
    for x, y in pts:
        g[y][x] = ch


def overlay(dst, src, skip_outline_on=None):
    for y in range(H):
        for x in range(W):
            c = src[y][x]
            if c == '.':
                continue
            if skip_outline_on and c in 'Ov' and dst[y][x] not in skip_outline_on:
                continue
            dst[y][x] = c


def stamp(g, x0, y0, rows, mirror=False):
    for dy, r in enumerate(rows):
        for dx, c in enumerate(r):
            put(g, x0 + dx, y0 + dy, c)
            if mirror:
                put(g, AX - (x0 + dx), y0 + dy, c)


def sym_rows(g, rows, ch):
    """rows: {y: halfwidth} around the axis (18.5)."""
    for y, w in rows.items():
        for x in range(19 - w, 19 + w):
            put(g, x - 1 + 1, y, ch) if False else put(g, x, y, ch)


# ---------------- veil (behind everything) ----------------
VEIL_R = {8: 28, 9: 29, 10: 30, 11: 30, 12: 31, 13: 31, 14: 31, 15: 32, 16: 33, 17: 33, 18: 34, 19: 34,
          20: 34, 21: 35, 22: 35, 23: 35, 24: 36, 25: 36, 26: 36, 27: 36, 28: 37, 29: 37, 30: 37,
          31: 37, 32: 37, 33: 37, 34: 38, 35: 38, 36: 38, 37: 38}
VEIL_R.update({y: 39 for y in range(38, 48)})
VEIL_R.update({48: 38, 49: 37})


def veil():
    g = blank()
    for y, r in VEIL_R.items():
        left = 9 if y < 30 else (2 if y < 48 else 3)
        for x in range(left, r + 1):
            g[y][x] = 'V'
    # soft folds
    for y in range(20, 48):
        for x in (33, 36):
            if g[y][x] == 'V' and (y + x) % 7 != 0:
                g[y][x] = 'v' if x == 36 and y > 34 else g[y][x]
    outline(g, 'Vv', 'v')
    return g


# ---------------- gown + bodice + arms ----------------
GOWN = {46: 10, 47: 11, 48: 12, 49: 13, 50: 13, 51: 14, 52: 14, 53: 14, 54: 15, 55: 15,
        56: 15, 57: 15, 58: 16, 59: 16, 60: 16, 61: 16, 62: 15}


def dress():
    g = blank()
    # bare shoulders / arms (skin) rows 37-47
    arms = {37: 8, 38: 9, 39: 9, 40: 9, 41: 9, 42: 9, 43: 9, 44: 9, 45: 8}
    for y, w in arms.items():
        for x in range(19 - w, 19 + w):
            g[y][x] = 'S'
    # bodice: sweetheart neckline
    bod = {40: 5, 41: 6, 42: 6, 43: 6, 44: 7, 45: 7}
    for y, w in bod.items():
        for x in range(19 - w, 19 + w):
            g[y][x] = 'D'
    for x in (18, 19):
        g[40][x] = 'S'          # dip of the sweetheart line
    for y, w in GOWN.items():
        for x in range(19 - w, 19 + w):
            g[y][x] = 'D'
    # folds (symmetric) + hem shade
    for y in range(50, 62):
        for dx in (6, 11):
            if y >= 50 + dx // 3:
                put(g, 19 - dx - 1 + (y - 50) // 6 * -1 + 0, y, 'd')
                put(g, AX - (19 - dx - 1 + (y - 50) // 6 * -1), y, 'd')
        put(g, 18, y, 'd') if y > 53 else None
    for y, w in GOWN.items():
        put(g, 19 - w, y, 'e')
        put(g, 18 + w, y, 'e')
    for x in range(19 - GOWN[62], 19 + GOWN[62]):
        g[62][x] = 'e'
    # arm shading + skin outline
    for y in range(38, 46):
        put(g, 10, y, 's')
        put(g, 27, y, 's')
    outline(g, 'S', 'k')
    outline(g, 'Dde', 'O')
    return g


# ---------------- face ----------------
FACE = {y: 9 for y in range(17, 34)}
FACE.update({34: 9, 35: 8, 36: 7, 37: 5})


def face():
    g = blank()
    for y, w in FACE.items():
        for x in range(19 - w, 19 + w):
            g[y][x] = 'S'
    for y in range(30, 34):      # ears
        put(g, 9, y, 'S')
        put(g, 28, y, 'S')
    for y in (35, 36, 37):
        put(g, 19 - FACE[y], y, 's')
        put(g, 18 + FACE[y], y, 's')
    outline(g, 'S', 'k')
    eye = ['.EE.', 'EWEE', 'EEEE', 'EIIE', '.EE.']
    stamp(g, 11, 29, eye)
    stamp(g, AX - 14, 29, eye)
    put(g, 10, 29, 'E')          # lashes
    put(g, AX - 10, 29, 'E')
    stamp(g, 10, 34, ['.BB.', 'BBBB'], mirror=True)
    stamp(g, 17, 35, ['M..M', '.MM.'])
    return g


def hair():
    _, lum = underlay((86, 22, 192, 176), 44, shift=0)
    import numpy as np
    lum = np.pad(lum, ((0, 0), (0, 4)), constant_values=255)[:, -SHIFT:]

    def allow(x, y):
        if x < 4 or x > 33 or y < 7 or y > 46:
            return False
        in_face = y in FACE and 19 - FACE[y] <= x < 19 + FACE[y]
        if in_face and y >= 27:
            return False
        if y >= 38 and 12 <= x <= 25:   # bodice / bouquet area
            return False
        if 8 <= x <= 9 and 30 <= y <= 33 or 28 <= x <= 29 and 30 <= y <= 33:
            return False                # ears
        return True
    g = hair_grid(lum, allow, W, H, light=52)
    outline(g, 'Hh', 'O')
    return g


BOUQUET = [
    '...eeee...',
    '..eRRrRe..',
    '.eRrRRRre.',
    'eRRRrRRrRe',
    'eRrRRRRRre',
    'eRRRrRrRRe',
    'GgRRRRRRgG',
    'GGgRrRRgGG',
    '.GGgRRgGG.',
    '..GGggGG..',
    '...GggG...',
    '....GG....',
]


def tiara(g):
    stamp(g, 14, 9, ['.PpPpPpPp.', 'Pp......pP'])
    stamp(g, 16, 8, ['.PP..PP.'])


def bride():
    g = veil()
    overlay(g, dress())
    f = face()
    for y in range(H):
        for x in range(W):
            if f[y][x] == 'k' and g[y][x] == 'S':
                f[y][x] = 's'          # chin meets the shoulders: soft shade, not a line
    overlay(g, f)
    overlay(g, hair(), skip_outline_on='.kVv')
    # hands on the bouquet
    stamp(g, 12, 45, ['kSS'])
    stamp(g, 23, 45, ['SSk'])
    stamp(g, 14, 41, BOUQUET)
    tiara(g)
    return g


def save(g, name):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            c = g[y][x]
            if c == '.':
                continue
            if c == 'V':
                im.putpixel((x, y), (250, 249, 255, 190))
            else:
                im.putpixel((x, y), PAL[c] + (255,))
    im.save(name)


if __name__ == '__main__':
    save(bride(), 'hand_bride.png')
