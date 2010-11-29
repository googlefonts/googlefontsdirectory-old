#!/usr/bin/python
#
# With the SFDs in the current directory, run this with
# $ python generate.py

import fontforge, sys
required_version = "20090923"

if fontforge.version() < required_version:
  print ("Your version of FontForge is too old - %s or newer is required" % (required_version));

print ("Current fontforge version:")
print fontforge.version()

files = [
	'Puritan-BoldItalic.sfd',
	'Puritan-Bold.sfd',
	'Puritan-Italic.sfd',
	'Puritan-Regular.sfd'
]

for font in files:
    f = fontforge.open(font)    
    print ("Building   ") + f.fullname + ( " ") + f.weight + ("  from sfd sources with fontforge")
    f.em = 1024
    f.round()
    f.selection.all()
    f.autoHint()
    f.autoInstr()
    f.generate(f.fontname + ".otf",flags=("opentype"))
    f.close

print ("font version:")
print (f.version)

print ("Done");

