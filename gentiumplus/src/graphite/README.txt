README
Gentium Plus v1.504
========================

This file describes the Graphite source files included with the Gentium Plus font family. This information should be distributed along with the Gentium Plus fonts and any derivative works.

As a reminder: these source files are Copyright (c) 2003-2010 SIL International
(http://www.sil.org/), with Reserved Font Names "Gentium" and "SIL".
This Font Software is licensed under the SIL Open Font License, Version 1.1.
            
font.gdl              - definition of glyphs and glyph classes; auto-generated from the font
main.gdh              - bulk of Graphite rules and extra definitions to support them
features.gdh          - feature and language-feature definitions
pitches.gdh           - rules and definitions to support tone ligatures
pua.gdh               - mapping from PUA pseudo-glyphs to real Unicode glyphs
greek_recompose.gdh   - rules to recompose decomposed Greek
takes_lowProfile.gdh  - definitions to support low-profile feature; auto-generated
fontSpecific.gdh      - font-specific definition for Gentium
stddef.gdh            - standard GDL abbreviations

In order to modify the Graphite tables in this font:
* Strip out the existing tables
  Using the Font-TTF-Scripts package ( http://scripts.sil.org/FontUtils ), you could use something like:
    ttftable -delete Feat,Glat,Gloc,Silf,Sill <ttf-file-with-Graphite-tables>  <ttf-file-with-Graphite-tables-stripped>
* Run:
    grcompiler -d -v2 -n2048 -w3521 -w510 font.gdl <ttf-file-with-Graphite-tables-stripped> <output-ttf>
    