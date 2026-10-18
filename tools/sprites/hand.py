"""Hand-built chibi pixel sprites (32 x 42), layered: body / face / hair / outfit."""
from PIL import Image

W, H = 32, 42
AX = 31  # mirror: x -> AX - x

PAL = {
    'O': (20, 18, 22), 'k': (160, 96, 79),
    'S': (255, 226, 204), 's': (242, 191, 160),
    'B': (247, 161, 168), 'M': (181, 85, 95),
    'E': (20, 18, 22), 'I': (78, 74, 86), 'W': (255, 255, 255),
    'H': (34, 32, 37), 'h': (74, 72, 80), 'j': (118, 116, 126),
    'T': (40, 40, 45), 't': (74, 74, 82),
    'C': (255, 255, 255), 'c': (220, 216, 234),
    'D': (255, 255, 255), 'd': (231, 227, 241), 'e': (201, 194, 220),
    'v': (214, 209, 230), 'V': (250, 249, 255),
    'G': (111, 157, 85), 'g': (166, 201, 122), 'R': (255, 246, 240), 'r': (243, 217, 222),
    'P': (255, 255, 255), 'p': (207, 200, 224), 'F': (14, 13, 16),
}


def blank():
    return [['.'] * W for _ in range(H)]


def put(g, x, y, c):
    if 0 <= x < W and 0 <= y < H and c != '.':
        g[y][x] = c


def sym_fill(g, rows, ch):
    """rows: {y: halfwidth} -> filled symmetric span around the centre line."""
    for y, w in rows.items():
        for x in range(16 - w, 16 + w):
            put(g, x, y, ch)


def outline(g, fill_chars, ch, diag=False):
    """Outside 4-neighbour outline -> clean 1px stair lines."""
    out = []
    for y in range(H):
        for x in range(W):
            if g[y][x] != '.':
                continue
            nb = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            if any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] in fill_chars for dy, dx in nb):
                out.append((x, y))
    for x, y in out:
        g[y][x] = ch


def overlay(dst, src):
    for y in range(H):
        for x in range(W):
            if src[y][x] != '.':
                dst[y][x] = src[y][x]


def stamp(g, x0, y0, rows, mirror=False):
    for dy, r in enumerate(rows):
        for dx, c in enumerate(r):
            put(g, x0 + dx, y0 + dy, c)
            if mirror:
                put(g, AX - (x0 + dx), y0 + dy, c)


def from_rows(rows, y0=0):
    g = blank()
    for dy, r in enumerate(rows):
        for x, c in enumerate(r):
            put(g, x, y0 + dy, c)
    return g


# ---------- base: head skin + ears + body skin (hands / legs) ----------
FACE_HW = {8: 9, 9: 11, 10: 12, 11: 12}
FACE_HW.update({y: 12 for y in range(12, 21)})
FACE_HW.update({21: 12, 22: 11, 23: 11, 24: 10, 25: 8, 26: 6, 27: 3})


def base_head():
    g = blank()
    sym_fill(g, FACE_HW, 'S')
    # ears
    for y in range(17, 22):
        for x in (2, 3):
            put(g, x, y, 'S')
            put(g, AX - x, y, 'S')
    outline(g, 'S', 'k')
    # soft shade: right/bottom rim of the face (light from top-left)
    for y, w in FACE_HW.items():
        if y >= 22:
            put(g, 16 + w - 1, y, 's')
            put(g, 16 - w, y, 's')
    for y in range(18, 21):
        put(g, 3, y, 's')
        put(g, AX - 3, y, 's')
    return g


def face(lashes=False):
    g = blank()
    eye = ['.EE.', 'EWEE', 'EEEE', 'EIIE', '.EE.']
    stamp(g, 8, 16, eye)
    stamp(g, AX - 11, 16, [r[::-1] for r in eye])
    if lashes:
        put(g, 7, 16, 'E')
        put(g, AX - 7, 16, 'E')
    stamp(g, 8, 13, ['hhh'])
    stamp(g, AX - 10, 13, ['hhh'])
    stamp(g, 6, 22, ['.BB.', 'BBBB'], mirror=True)
    stamp(g, 14, 23, ['M..M', '.MM.'])
    return g


if __name__ == '__main__':
    import sys
    g = base_head()
    overlay(g, face())
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            c = g[y][x]
            if c != '.':
                im.putpixel((x, y), PAL[c] + (255,))
    im.save('hand_test.png')


def overlay_hair(dst, hair):
    """Hair outline only lands on empty space or the face outline, never on skin."""
    for y in range(H):
        for x in range(W):
            c = hair[y][x]
            if c == '.':
                continue
            if c == 'O' and dst[y][x] not in '.k':
                continue
            dst[y][x] = c


def hair_mass(outer_hw, bangs, side_bottom):
    """outer_hw: {y: halfwidth} silhouette; bangs: {x: first visible face row};
    side_bottom: hair end row for columns outside the face."""
    g = blank()
    for y, w in outer_hw.items():
        for x in range(16 - w, 16 + w):
            limit = bangs.get(x, side_bottom)
            if y < limit:
                g[y][x] = 'H'
    return g


def shade_hair(g, highlights, strands=()):
    for x, y, c in highlights:
        if g[y][x] == 'H':
            g[y][x] = c
    for pts in strands:
        for x, y in pts:
            if g[y][x] in 'Hh':
                g[y][x] = 'h'


GROOM_OUTER = {0: 5, 1: 8, 2: 10, 3: 12, 4: 13, 5: 14, 6: 14}
GROOM_OUTER.update({y: 15 for y in range(7, 17)})
# comma hair (half-exposed forehead): part at x=12, right bangs sweep down and curl in
GROOM_BANGS = dict(zip(range(4, 28), [15, 13, 10, 9, 8, 8, 8, 8, 8, 9, 10, 11, 12, 13, 14, 15,
                                         15, 15, 14, 12, 12, 13, 15, 16]))


def groom_hair():
    g = hair_mass(GROOM_OUTER, GROOM_BANGS, 17)
    hl = [(x, 3, 'h') for x in range(7, 12)] + [(x, 4, 'h') for x in range(5, 9)] + \
         [(8, 3, 'j'), (9, 3, 'j'), (6, 4, 'j')]
    # comma sweep: two strands following the curl from the part down to the tip
    strands = [[(13, 4), (14, 5), (15, 6), (16, 7), (17, 8), (18, 9), (19, 10), (20, 11)],
               [(13, 7), (14, 8), (15, 9), (16, 10), (17, 11), (18, 12)],
               [(21, 5), (22, 6), (23, 7), (24, 8), (25, 9)]]
    shade_hair(g, hl, strands)
    # comma tip: the strand hooks back inward
    for x, y in [(19, 12), (20, 13), (21, 13)]:
        if g[y][x] in 'Hh':
            g[y][x] = 'h'
    # hairline above the exposed forehead
    outline(g, 'Hhj', 'O')
    return g


def mirror_rows(left):
    return [r + r[::-1] for r in left]


GROOM_BODY = mirror_rows([
    '......OOOOOOtOOC',
    '....OOTTTTTtCOOO',
    '...OtTTTTTTTtOOC',
    '...OtTTOTTTTTtCC',
    '...OtTTOTTTTTTtC',
    '...OtTTOTTTTTTTt',
    '...OtTTOTTTTTTTT',
    '...kSSSkTTTTTTTT',
    '....kkk.OOOOOOOO',
    '.........OtTTTTO',
    '.........OtTTTTO',
    '.........OtTTTTO',
    '.........OFFFFFO',
    '..........OOOOO.',
])


def groom():
    g = base_head()
    overlay(g, face())
    overlay_hair(g, groom_hair())
    overlay(g, from_rows(GROOM_BODY, 28))
    # boutonniere (white flower, viewer's right lapel)
    stamp(g, 20, 31, ['RR', 'Rg'])
    return g


def save(g, name):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            c = g[y][x]
            if c != '.':
                im.putpixel((x, y), PAL[c] + (255,))
    im.save(name)
