#!/usr/bin/env python
#
# setprep-fontforge.py
#
# Copyright (c) 2011 Dave Crossland <dave@understandinglimited.com>
#
# This program takes a TTF font with no hinting and sets
# its PREP hinting table with magic values that turn on 
# 'drop out control' - the magic comes from Raph Levien 
# <firstname.lastname@gmail.com> and is:
#
# PUSHW_1
#  511
# SCANCTRL
# PUSHB_1
#  4
# SCANTYPE
#
# This script depends on the FontForge Python library, available
# in most packaging systems and sf.net/projects/fontforge/ 
#
# Usage:
#
# $ ./setprep-fontforge.py FontIn.ttf [FontOut.ttf]

# Import our system library and fontTools ttLib
import sys, fontforge

def getprep(font):
    prepAsm = font.getTableData("prep")
    prepText = fontforge.unParseTTInstrs(prepAsm)
    return prepText

def main(argv):
#   Open the font file supplied as the first argument on the command line
    font_in = argv[1]
    font = fontforge.open(font_in)
#   If there is a second font file specified on the command line, output to that
    if argv[2]:
        font_out = argv[2]
#   Else, update the file
    else:
        font_out = font_in

#   Print the existing PREP table
    print "The PREP table is:"
    print getprep(font)

#   Set PREP to magic prep
    prepTextMagic = """PUSHW_1
     511
    SCANCTRL
    PUSHB_1
     4
    SCANTYPE"""
    prepAsmMagic = fontforge.parseTTInstrs(prepTextMagic)
    font.setTableData("prep",prepAsmMagic)

#   Print the existing PREP table
    print "The PREP table is now:"
    print getprep(font)

#   Generate the new font with no hinting instructions
    flags = ('omit-instructions',)
    font.generate(font_out, flags = flags)
    print "in file", font_out, " - done!"

if __name__ == '__main__':
    main(sys.argv)