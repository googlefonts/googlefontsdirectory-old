#!/usr/bin/env python
#
# setnonhinting-fontforge.py
#
# Copyright (c) 2011 Dave Crossland <dave@understandinglimited.com>
#
# This program takes a TTF font with no hinting and sets
# its hinting tables with magic values that turn on 
# rendering features that provide optimal font display. 
#
# The magic is in two places: 
#
# 1. The GASP table. Vern Adams <vern@newtypography.co.uk>
#    suggests it should have value 15 for all sizes, which
#    means turning everything on.
#
# 2. The PREP table. Raph Levien <firstname.lastname@gmail.com>
#    suggests using his code to turn on 'drop out control'
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
# $ ./setnonhinting-fontforge.py FontIn.ttf [FontOut.ttf]

# Import our system library and fontTools ttLib
import sys, fontforge

def getprep(font):
    if font.getTableData("prep") == None:
        return "None"
    prepAsm = font.getTableData("prep")
    prepText = fontforge.unParseTTInstrs(prepAsm)
    return prepText

def main(argv):
#   Open the font file supplied as the first argument on the command line
    font_in = argv[0]
    font = fontforge.open(font_in)

#   Print the existing PREP table
    print font.path, "PREP table contains:"
    print getprep(font)

#   Print the existing GASP table
    print "The GASP table is version", font.gasp_version, "and contains:", font.gasp

#   Set the GASP table to turn everything on and version to 1
    font.gasp = ((65535, ('gridfit', 'antialias', 'symmetric-smoothing', 'gridfit+smoothing')),)
# TODO 2011-03-28 DC This doesn't appear work, but that appears not to matter. 
    font.gasp_version = 1

#   Set PREP to magic prep
    prepTextMagic = """PUSHW_1
     511
    SCANCTRL
    PUSHB_1
     4
    SCANTYPE"""
    prepAsmMagic = fontforge.parseTTInstrs(prepTextMagic)
    font.setTableData("prep",prepAsmMagic)


#   If there is a second font file specified on the command line, output to that
    if len(argv) == 2:
        font_out = argv[1]
#   Else, update the file
    else:
        font_out = font_in
#   If we opened a SFD, save it
    if font_in[-3:] == "sfd" or "SFD":
        font.save(font_out)
#   Else if we opened a TTF, generate the new font with no hinting instructions
    if font_in[-3:] == "ttf" or "TTF" or "otf" or "OTF":
        flags = ('omit-instructions',)
        font.generate(font_out, flags = flags)

#   Print the PREP table of the output font
    font = fontforge.open(font_out)
    print ""
    print ""
    print font.path, "PREP table now contains:"
    print getprep(font)
    print "The GASP table is version", font.gasp_version, "and contains:", font.gasp


if __name__ == '__main__':
    main(sys.argv[1:3])
