#!/usr/bin/python
#
# When SFDs are in current directory, run this with
# $ python generate.py

import fontforge

files = [
'PuritanBoldItalic.sfd',
'PuritanBold.sfd',
'PuritanItalic.sfd',
'Puritan.sfd'
]

for font in files:
    f = fontforge.open(font)
    f.generate(f.fontname + '.otf')
    f.em = 1024
    f.round()
    f.selection.all()
    f.autoHint()
    f.autoInstr()
    f.generate(f.fontname + '.ttf')
