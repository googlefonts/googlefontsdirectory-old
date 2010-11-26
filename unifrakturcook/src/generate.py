#!/usr/bin/python

import fontforge

files = [
'UnifrakturCook.sfd',
]

for font in files:
    f = fontforge.open(font)
    f.generate(f.fontname + '.ttf')
