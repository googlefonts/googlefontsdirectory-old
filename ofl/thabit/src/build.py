#!/usr/bin/env python
# coding: UTF-8
import fontforge
import os
import tempfile

release = "0.3"
fea     = "Thabit.fea"
Flags   = ("opentype",)

def generate(arfont, ltfont):
	font = fontforge.open(arfont)
	font.mergeFeature(fea)
	font.mergeFonts(ltfont)
	font.copyright = font.copyright + "\nLatin glyphs are Copyright (c) IBM Corporation 1990,1991."
	font.version   = release
	print "Generating '%s'" % font.fullname
	font.generate(font.fontname + ".ttf", flags=Flags)
	font.close()

def obliqize(infont, outfont, angle, family, arfamily):
	font = fontforge.open(infont)
	import psMat
	skew = psMat.skew(angle)
	for glyph in font.glyphs():
		if glyph.isWorthOutputting():
			font.selection.select(("more", "singletons"), glyph.glyphname)
	font.selection.select(("less", "ranges"), "afii61664", "afii61575")
	font.unlinkReferences()
	font.transform(skew)
	font.familyname = font.fontname = font.fontname + "-Oblique"
	font.fullname   = font.fullname + " Oblique"
	font.familyname = family
	font.appendSFNTName('Arabic (Egypt)', 'SubFamily', arfamily)
	font.save(outfont)
	font.close()

def deobliqize(outfont, infont):
	glyphs = ("parenleft", "parenright", "exclam",
			"bracketleft", "bracketright",
			"braceleft", "braceright",)
	font = fontforge.open(infont)
	for glyph in glyphs:
		font.selection.select(("more", "singletons"), glyph)
	font.copy()

	font2 = fontforge.open(outfont)
	for glyph in glyphs:
		font2.selection.select(("more", "singletons"), glyph)
	font2.paste()
	font.close()
	font2.save(outfont)

def build():
	# reglar
	generate("Thabit.sfd", "cour/cour.pfa")

	# bold
	generate("Thabit-Bold.sfd", "cour/courb.pfa")

	norm = tempfile.mkstemp()[1]
	bold = tempfile.mkstemp()[1]

	# oblique
	obliqize("Thabit.sfd", norm, -16, "Oblique", "مائل")
	deobliqize(norm, "cour/cour.pfa")
	generate(norm, "cour/couri.pfa")

	# bold-oblique
	obliqize("Thabit-Bold.sfd", bold, -16, "Bold Oblique", "عريض مائل")
	deobliqize(bold, "cour/courb.pfa")
	generate(bold, "cour/courbi.pfa")

	thb = "Thabit-"+release
	if not os.path.exists(thb):
		os.makedirs(thb)
	os.system("mv *.ttf %s" % thb)
	os.system("cp OFL.txt ChangeLog README* %s" % thb)

if __name__ == '__main__':
	build()
