#!/usr/bin/python

import fontforge

files = [
'UnifrakturMaguntia.sfd',
]

for font in files:
    f = fontforge.open(font)
    f.generate(f.fontname + '.ttf')
