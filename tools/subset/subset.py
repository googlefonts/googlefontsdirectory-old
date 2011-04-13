#!/usr/bin/python

# Copyright 2010, Google Inc.
# Author: Raph Levien (<firstname.lastname>@gmail.com)
# Author: Dave Crossland (dave@understandinglimited.com)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# A script for subsetting a font, using FontForge. See README for details.

import fontforge
import sys
import getopt
import os
import struct

def select_with_refs(font, unicode, newfont, pe = None, nam = None):
    newfont.selection.select(('more', 'unicode'), unicode)
    if nam:
        print >> nam, "0x%0.4X" % unicode, fontforge.nameFromUnicode(unicode)
    if pe:
        print >> pe, "SelectMore(%d)" % unicode
    try:
        for ref in font[unicode].references:
            #print unicode, ref
            newfont.selection.select(('more',), ref[0])
            if nam:
                print >> nam, "0x%0.4X" % ref[0], fontforge.nameFromUnicode(ref[0])
            if pe:
                print >> pe, 'SelectMore("%s")' % ref[0]
    except:
        print 'Resolving references on u+%04x failed' % unicode

def subset_font_raw(font_in, font_out, unicodes, opts):
    if '--namelist' in opts:
        # 2010-12-06 DC To allow setting namelist filenames, 
        # change getopt.gnu_getopt from namelist to namelist= 
        # and invert comments on following 2 lines
        # nam_fn = opts['--namelist']
        nam_fn = font_out + '.nam'
        nam = file(nam_fn, 'w')
    else:
        nam = None
    if '--script' in opts:
        pe_fn = "/tmp/script.pe"
        pe = file(pe_fn, 'w')
    else:
        pe = None
    font = fontforge.open(font_in)
    if pe:
      print >> pe, 'Open("' + font_in + '")'
      extract_vert_to_script(font_in, pe)
    for i in unicodes:
        select_with_refs(font, i, font, pe, nam)

    addl_glyphs = []
    if '--nmr' in opts: addl_glyphs.append('nonmarkingreturn')
    if '--null' in opts: addl_glyphs.append('.null')
    for glyph in addl_glyphs:
        font.selection.select(('more',), glyph)
        if nam:
            print >> nam, "0x%0.4X" % fontforge.unicodeFromName(glyph), glyph
        if pe:
            print >> pe, 'SelectMore("%s")' % glyph

    flags = ()

    if '--simplify' in opts:
        font.simplify()
        font.round()
        flags = ('omit-instructions',)

    if '--strip_names' in opts:
        font.sfnt_names = ()

    if '--new' in opts:
        font.copy()
        new = fontforge.font()
        new.encoding = font.encoding
        new.em = font.em
        new.layers['Fore'].is_quadratic = font.layers['Fore'].is_quadratic
        for i in unicodes:
            select_with_refs(font, i, new, pe, nam)
        new.paste()
        # This is a hack - it should have been taken care of above.
        font.selection.select('space')
        font.copy()
        new.selection.select('space')
        new.paste()
        new.sfnt_names = font.sfnt_names
        font = new
    else:
        font.selection.invert()
        print >> pe, "SelectInvert()"
        font.cut()
        print >> pe, "Clear()"

    if nam: 
        print "Writing NameList", 
        nam.close()

    if pe:
        print >> pe, 'Generate("' + font_out + '")'
        pe.close()
        os.system("fontforge -script " + pe_fn)
    else:
        font.generate(font_out, flags = flags)
    font.close()

    if '--roundtrip' in opts:
        # FontForge apparently contains a bug where it incorrectly calculates
        # the advanceWidthMax in the hhea table, and a workaround is to open
        # and re-generate
        font2 = fontforge.open(font_out)
        font2.generate(font_out, flags = flags)

def subset_font(font_in, font_out, unicodes, opts):
    font_out_raw = font_out
    if not font_out_raw.endswith('.ttf'):
        font_out_raw += '.ttf';
    subset_font_raw(font_in, font_out_raw, unicodes, opts)
    if font_out != font_out_raw:
        os.rename(font_out_raw, font_out)
# 2011-02-14 DC this needs to only happen with --namelist is used
#        os.rename(font_out_raw + '.nam', font_out + '.nam')

def getsubset(subset):
    subsets = subset.split('+')

    quotes  = [0x2013] # endash
    quotes += [0x2014] # emdash
    quotes += [0x2018] # quoteleft
    quotes += [0x2019] # quoteright
    quotes += [0x201A] # quotesinglbase
    quotes += [0x201C] # quotedblleft
    quotes += [0x201D] # quotedblright
    quotes += [0x201E] # quotedblbase
    quotes += [0x2022] # bullet
    quotes += [0x2039] # guilsinglleft
    quotes += [0x203A] # guilsinglright

    latin  = range(0x20, 0x7f) # Basic Latin (A-Z, a-z, numbers)
    latin += range(0xa0, 0x100) # Western European symbols and diacritics
    latin += [0x20ac] # Euro
    latin += [0x0152] # OE
    latin += [0x0153] # oe
    latin += [0x003b] # semicolon
    latin += [0x00b7] # periodcentered
    latin += [0x0131] # dotlessi
    latin += [0x02c6] # circumflex
    latin += [0x02da] # ring
    latin += [0x02dc] # tilde
    latin += [0x2074] # foursuperior
    latin += [0x2215] # divison slash
    latin += [0x2044] # fraction slash
    latin += [0xe0ff] # PUA: Font logo
    latin += [0xeffd] # PUA: Font version number
    latin += [0xf000] # PUA: font ppem size indicator: run `ftview -f 1255 10 Ubuntu-Regular.ttf` to see it in action!

    result = quotes
    if 'latin' in subset:
        result += latin
    if 'latin-ext' in subset:
        # These ranges include Extended A, B, C, D, and Additional with the
        # exception of Vietnamese, which is a separate range
        result += (range(0x100, 0x370) +
                   range(0x1d00, 0x1ea0) +
                   range(0x1ef2, 0x1f00) +
                   range(0x2070, 0x20d0) +
                   range(0x2c60, 0x2c80) +
                   range(0xa700, 0xa800))
    if 'vietnamese' in subset:
        result += range(0x1ea0, 0x1ef2) + [0x20ab]
    if 'greek' in subset:
        # Could probably be more aggressive here and exclude archaic characters,
        # but lack data
        result += range(0x370, 0x400)
    if 'greek-ext' in subset:
        result += range(0x370, 0x400) + range(0x1f00, 0x2000)
    if 'cyrillic' in subset:
        # Based on character frequency analysis
        result += range(0x400, 0x460) + [0x490, 0x491, 0x4b0, 0x4b1]
    if 'cyrillic-ext' in subset:
        result += (range(0x400, 0x530) +
                   [0x20b4] +
                   range(0x2de0, 0x2e00) +
                   range(0xa640, 0xa6a0))
    return result

# code for extracting vertical metrics from a TrueType font

class Sfnt:
    def __init__(self, data):
        version, numTables, _, _, _ = struct.unpack('>IHHHH', data[:12])
        self.tables = {}
        for i in range(numTables):
            tag, checkSum, offset, length = struct.unpack('>4sIII', data[12 + 16 * i: 28 + 16 * i])
            self.tables[tag] = data[offset: offset + length]

    def hhea(self):
        r = {}
        d = self.tables['hhea']
        r['Ascender'], r['Descender'], r['LineGap'] = struct.unpack('>hhh', d[4:10])
        return r

    def os2(self):
        r = {}
        d = self.tables['OS/2']
        r['fsSelection'], = struct.unpack('>H', d[62:64])
        r['sTypoAscender'], r['sTypoDescender'], r['sTypoLineGap'] = struct.unpack('>hhh', d[68:74])
        r['usWinAscender'], r['usWinDescender'] = struct.unpack('>HH', d[74:78])
        return r

def set_os2(pe, name, val):
    print >> pe, 'SetOS2Value("' + name + '", %d)' % val

def set_os2_vert(pe, name, val):
    set_os2(pe, name + 'IsOffset', 0)
    set_os2(pe, name, val)

# Extract vertical metrics data directly out of font file, and emit
# script code to set the values in the generated font. This is a (rather
# ugly) workaround for the issue described in:
# http://sourceforge.net/mailarchive/forum.php?thread_name=20100906085718.GB1907%40khaled-laptop&forum_name=fontforge-users

def extract_vert_to_script(font_in, pe):
    data = file(font_in, 'rb').read()
    sfnt = Sfnt(data)
    hhea = sfnt.hhea()
    os2 = sfnt.os2()
    set_os2_vert(pe, "WinAscent", os2['usWinAscender'])
    set_os2_vert(pe, "WinDescent", os2['usWinDescender'])
    set_os2_vert(pe, "TypoAscent", os2['sTypoAscender'])
    set_os2_vert(pe, "TypoDescent", os2['sTypoDescender'])
    set_os2_vert(pe, "HHeadAscent", hhea['Ascender'])
    set_os2_vert(pe, "HHeadDescent", hhea['Descender'])

def main(argv):
    optlist, args = getopt.gnu_getopt(argv, '', ['string=', 'strip_names',
                                                 'simplify', 'new', 'script',
                                                 'nmr', 'roundtrip', 'subset=',
                                                 'namelist', 'null'])

    font_in, font_out = args
    opts = dict(optlist)
    if '--string' in opts:
        subset = map(ord, opts['--string'])
    else:
        subset = getsubset(opts.get('--subset', 'latin'))
    subset_font(font_in, font_out, subset, opts)

if __name__ == '__main__':
    main(sys.argv[1:])
