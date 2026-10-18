import sys
tpl = open('index.tpl.html').read()
out = tpl.replace('__SPRITES__', open('sprites.json').read()).replace('__ENGINE__', open('engine.js').read())
open(sys.argv[1] if len(sys.argv) > 1 else '../../index.html', 'w').write(out)
print(len(out))
