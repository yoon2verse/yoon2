"""Render one or more sprite PNGs zoomed with a faint pixel grid, plus 1x/2x/3x previews."""
import sys
from PIL import Image, ImageDraw
out = sys.argv[1]
ims = [Image.open(p).convert('RGBA') for p in sys.argv[2:]]
S = 12
bgc = (239, 228, 212, 255)
w = sum(i.width for i in ims) * S + 20 * (len(ims) + 1)
h = max(i.height for i in ims) * S + 40 + max(i.height for i in ims) * 3 + 20
sheet = Image.new('RGBA', (w, h), bgc)
d = ImageDraw.Draw(sheet)
x = 20
for im in ims:
    big = im.resize((im.width * S, im.height * S), Image.NEAREST)
    sheet.alpha_composite(big, (x, 20))
    for gx in range(im.width + 1):
        d.line([(x + gx * S, 20), (x + gx * S, 20 + big.height)], fill=(0, 0, 0, 18))
    for gy in range(im.height + 1):
        d.line([(x, 20 + gy * S), (x + big.width, 20 + gy * S)], fill=(0, 0, 0, 18))
    x += big.width + 20
x = 20
y = 40 + max(i.height for i in ims) * S
for s in (1, 2, 3):
    for im in ims:
        sm = im.resize((im.width * s, im.height * s), Image.NEAREST)
        sheet.alpha_composite(sm, (x, y + max(i.height for i in ims) * 3 - sm.height))
        x += sm.width + 4
    x += 30
sheet.save(out)
