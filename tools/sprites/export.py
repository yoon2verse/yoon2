"""Build every sprite part as char grids and export them as a JS data block."""
import json
import hand2
import bride as B
from hand import mirror_rows

W, H = 32, 63
AX = 31


def blank():
    return [['.'] * W for _ in range(H)]


def rows(g):
    return [''.join(r) for r in g]


def outline(g, fill, ch):
    pts = [(x, y) for y in range(H) for x in range(W) if g[y][x] == '.' and any(
        0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] in fill
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in pts:
        g[y][x] = ch


def strip_outline(g, ch='O'):
    for y in range(H):
        for x in range(W):
            if g[y][x] == ch:
                g[y][x] = '.'


def place(rows_, y0):
    g = blank()
    for dy, r in enumerate(rows_):
        for x, c in enumerate(r):
            if c != '.':
                g[y0 + dy][x] = c
    return g


# ---------------- male head + hair ----------------
def m_head():
    g = hand2.base_head()
    f = hand2.face()
    for y in range(H):
        for x in range(W):
            if f[y][x] != '.':
                g[y][x] = f[y][x]
    for x in (7, 8, 9):                       # brows (hair may cover them)
        g[22][x] = 'h'
        g[22][AX - x] = 'h'
    return g


M_OUTER = {1: 4, 2: 7, 3: 9, 4: 11, 5: 12, 6: 13, 7: 14, 8: 14}
M_OUTER.update({y: 15 for y in range(9, 24)})
M_OUTER.update({y: 15 for y in range(24, 30)})
M_OUTER.update({30: 14})


def gen_hair(bangs, highlights):
    g = blank()
    for y, w in M_OUTER.items():
        for x in range(16 - w, 16 + w):
            if 5 <= x <= 26:
                if y < bangs[x]:
                    g[y][x] = 'H'
            elif x in (3, 4, 27, 28):
                if y < 24:
                    g[y][x] = 'H'
            elif y < 30 or x in (2, 29):
                g[y][x] = 'H'
    for x, y, c in highlights:
        if g[y][x] == 'H':
            g[y][x] = c
    outline(g, 'Hhj', 'O')
    return g


SHORT_BANGS = dict(zip(range(5, 27), [21, 19, 18, 17, 17, 18, 17, 17, 18, 17, 17, 17, 17, 18, 17, 17, 18,
                                       17, 17, 18, 19, 21]))
COMMA_BANGS = dict(zip(range(5, 27), [22, 20, 17, 15, 14, 14, 14, 14, 15, 16, 17, 18, 19, 20, 21, 21, 21,
                                       20, 19, 19, 20, 22]))
ARC = [(x, 4, 'h') for x in range(9, 14)] + [(x, 5, 'h') for x in range(6, 10)] + \
      [(x, 6, 'h') for x in range(4, 7)] + [(10, 4, 'j'), (11, 4, 'j'), (7, 5, 'j')] + \
      [(x, 5, 'h') for x in range(19, 23)] + [(x, 6, 'h') for x in range(22, 25)]


def m_hairs():
    part = hand2.hair()
    short = gen_hair(SHORT_BANGS, ARC + [(x, 15, 'h') for x in (8, 11, 14, 17, 20, 23)] +
                     [(x, 16, 'h') for x in (8, 11, 14, 17, 20, 23)])
    comma = gen_hair(COMMA_BANGS, ARC + [(x, y, 'h') for x, y in
                     [(12, 9), (13, 10), (14, 11), (15, 12), (16, 13), (17, 14), (18, 15), (19, 16),
                      (20, 17), (21, 18), (15, 9), (16, 10), (17, 11), (18, 12), (19, 13), (20, 14),
                      (21, 15), (22, 16)]])
    return {'part': part, 'short': short, 'comma': comma}


# ---------------- female head + hair (from the bride, shifted to the 32px canvas) ----------------
FSHIFT = 3


def shift(g42):
    g = blank()
    for y in range(H):
        for x in range(W):
            g[y][x] = g42[y][x + FSHIFT]
    return g


def f_head():
    return shift(B.face())


def f_hairs():
    long_ = shift(B.hair())
    # fill the hole the tiara left on the crown
    for y in range(0, 17):
        xs = [x for x in range(W) if long_[y][x] in 'Hh']
        if xs:
            for x in range(min(xs), max(xs) + 1):
                if long_[y][x] in '.O':
                    long_[y][x] = 'H'
    strip_outline(long_)

    def finish(g):
        outline(g, 'Hhj', 'O')
        return g

    def cut(src, last):
        g = [r[:] for r in src]
        for y in range(last + 1, H):
            g[y] = ['.'] * W
        return g

    bob = cut(long_, 37)
    bun = cut(long_, 31)
    for y, w in {1: 3, 2: 4, 3: 5, 4: 5, 5: 5, 6: 4}.items():
        for x in range(16 - w, 16 + w):
            bun[y][x] = 'H'
    for x, y in [(13, 2), (14, 2), (12, 3), (13, 3)]:
        bun[y][x] = 'h'
    return {'long': finish([r[:] for r in long_]), 'bob': finish(bob), 'bun': finish(bun)}


# ---------------- bodies ----------------
# letters: T top, t top light, d top dark, u collar light, C white inner, X tie,
#          P bottom, p bottom light, S skin, k skin line, F shoes, O outline
M_TOP = {
    'suit': mirror_rows([
        '......OOOOOOtCCX', '....OOTTTTTtCCCX', '...OtTTTTTTTtCCX', '..OtTTTTTTTTTtCX',
        '..OtTTTTTTTTTtCX', '.OtTTOTTTTTTTTtX', '.OtTTOTTTTTTTTtX', '.OtTTOTTTTTTTTTt',
        '.OtTTOTTTTTTTTTt', '.OtTTOTTTTTTTTTT', '.OtTTOTTTTTTTTTT', '.OtTTOTTTTTTTTTT',
        '.OtTTOTTTTTTTTTT', '.OCCCOTTTTTTTTTT', '.kSSSkTTTTTTTTTT', '.kSSSkTTTTTTTTTT',
        '..kkk.OTTTTTTTTT', '......OTTTTTTTTT', '......OOOOOOOOOO']),
    'shirt': mirror_rows([
        '......OOOOOOOuuO', '....OOTTTTTTOuuO', '...OtTTTTTTTTOud', '..OtTTTTTTTTTTTd',
        '..OtTTTTTTTTTTTW', '.OtTTOTTTTTTTTTd', '.OtTTOTTTTTTTTTd', '.OtTTOTTTTTTTTTW',
        '.OtTTOTTTTTTTTTd', '.OtTTOTTTTTTTTTd', '.OtTTOTTTTTTTTTW', '.OtTTOTTTTTTTTTd',
        '.OtTTOTTTTTTTTTd', '.OtuuOTTTTTTTTTd', '.kSSSkTTTTTTTTTd', '.kSSSkTTTTTTTTTd',
        '..kkk.OTTTTTTTTd', '......OTTTTTTTTd', '......OOOOOOOOOO']),
    'knit': mirror_rows([
        '......OOOOOOOddd', '....OOTTTTTTTOOO', '...OtTTTTTTTTTTT', '..OtTTTTTTTTTTTT',
        '..OtTTTTTTTTTTTT', '.OtTTOTTTTTTTTTT', '.OtTTOTTTTTTTTTT', '.OtTTOTTTTTTTTTT',
        '.OtTTOTTTTTTTTTT', '.OtTTOTTTTTTTTTT', '.OtTTOTTTTTTTTTT', '.OtTTOTTTTTTTTTT',
        '.OtTTOTTTTTTTTTT', '.OdddOTTTTTTTTTT', '.kSSSkTTTTTTTTTT', '.kSSSkTTTTTTTTTT',
        '..kkk.OTTTTTTTTT', '......OdddddddddO'[:16], '......OOOOOOOOOO']),
}
M_BOTTOM = {
    'pants': mirror_rows(['.......OpPPPPPPO'] * 7 + ['......OFFFFFFFFO'] * 2 + ['.......OOOOOOOO.']),
    'skirt': mirror_rows(['......OPPPPPPPPP', '.....OpPPPPPPPPP', '.....OpPPPPPPPPP',
                          '....OOOOOOOOOOOO', '.........kSSSk..', '.........kSSSk..',
                          '.........kSSSk..', '........OFFFFFO.', '........OFFFFFO.',
                          '.........OOOOO..']),
}
F_TOP = {
    'blouse': mirror_rows([
        '........OOOOkSSS', '......OOTTTuukSS', '.....OtTTTTTuukk', '....OtTTTTTTTTTd',
        '....OtTOTTTTTTTW', '....OtTOTTTTTTTd', '....OtTOTTTTTTTd', '....OtTOTTTTTTTW',
        '....OtTOTTTTTTTd', '....OtuOTTTTTTTd', '....kSSkTTTTTTTd', '....kSSkTTTTTTTd',
        '.....kk.OOOOOOOO']),
    'knit': mirror_rows([
        '........OOOOkSSS', '......OOTTTTTkSS', '.....OtTTTTTTTdd', '....OtTTTTTTTTTT',
        '....OtTOTTTTTTTT', '....OtTOTTTTTTTT', '....OtTOTTTTTTTT', '....OtTOTTTTTTTT',
        '....OtTOTTTTTTTT', '....OddOTTTTTTTT', '....kSSkTTTTTTTT', '....kSSkdddddddd',
        '.....kk.OOOOOOOO']),
    'jacket': mirror_rows([
        '........OOOOkSSS', '......OOTTTTtkSS', '.....OtTTTTTTtCC', '....OtTTTTTTTtCC',
        '....OtTOTTTTTTtC', '....OtTOTTTTTTtC', '....OtTOTTTTTTtC', '....OtTOTTTTTTTt',
        '....OtTOTTTTTTTt', '....OCCOTTTTTTTT', '....kSSkTTTTTTTT', '....kSSkTTTTTTTT',
        '.....kk.OOOOOOOO']),
}
F_BOTTOM = {
    'skirt': mirror_rows(['.......OPPPPPPPP', '......OPPPPPPPPP', '......OpPPPPPPPP',
                          '.....OpPPPPPPPPP', '.....OpPPPPPPPPP', '.....OOOOOOOOOOO',
                          '..........kSSk..', '..........kSSk..', '..........kSSk..',
                          '.........OFFFFO.', '.........OFFFFO.', '..........OOOO..']),
    'pants': mirror_rows(['.......OPPPPPPPP', '.......OPPPPPPPP'] + ['.......OpPPPPPPO'] * 7 +
                         ['.......OFFFFFFFO'] * 2 + ['........OOOOOOO.']),
}


def couple():
    groom = rows(hand2.groom())
    bride = rows(B.bride())
    return groom, bride


if __name__ == '__main__':
    groom, bride = couple()
    data = {
        'groom': groom, 'bride': bride,
        'm': {'head': rows(m_head()), 'hair': {k: rows(v) for k, v in m_hairs().items()},
              'top': M_TOP, 'bottom': M_BOTTOM, 'topY': 34, 'bottomY': 53},
        'f': {'head': rows(f_head()), 'hair': {k: rows(v) for k, v in f_hairs().items()},
              'top': F_TOP, 'bottom': F_BOTTOM, 'topY': 38, 'bottomY': 51},
    }
    for base in ('m', 'f'):
        for part in ('top', 'bottom'):
            for k, v in data[base][part].items():
                assert all(len(r) == 32 for r in v), (base, part, k, [len(r) for r in v])
    json.dump(data, open('sprites.json', 'w'))
    print('ok', len(json.dumps(data)))
