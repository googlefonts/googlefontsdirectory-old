#!/usr/bin/env python
"""
# Copyright (c) 2011 Charles Brandt [code at charlesbrandt dot com]
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# generate a pdf displaying a table listing of all fonts with the font name and sample text
#
# By: Charles Brandt [code at charlesbrandt dot com]
# On: *2011.10.07 11:08:05 
# 
# Requires:
# reportlab
#
# Sources:
# http://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/
#
# Thanks:
# Everyone who has contributed to the Google Fonts project!
#
# Usage:
# $ cd path/to/googlefontsdirectory;
# $ python tools/specimen/specimen.py;
"""

import os, re

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet

def check_ignore(item, ignores=[]):
    """
    take a string (item)
    and see if any of the strings in ignores list are in the item
    if so ignore it.
    """
    ignore = False
    for i in ignores:
        if i and re.search(i, item):
            #print "ignoring item: %s for ignore: %s" % (item, i)
            ignore = True
    return ignore

#Configurations:
fontpath = '.'
sample_size = 14
sample_text = "Breathe. Visualize. Imagine. Dream. Now."

styles=getSampleStyleSheet()

# to start fresh in looking for ignores:
# Note: this can take a while to run!
ignores = []
ignores = ['Bevan', 'NotoSans', 'Lobster', 'DroidSans', 'DroidSerif', 'Neucha', 'MavenProBlack', 'Maven', 'Astloch', 'Chewy', 'Ubuntu', 'ComingSoon', 'PTSerif', 'PT', 'Arvo', 'Walter', 'Amaranth', 'Crafty', 'Molengo', 'Reenie', 'Anton', 'Cherry', 'Dancing', 'Copse', 'Comfo', 'GFSDi', 'OpenS', 'Chivo', 'NewsC', 'Calli', 'Ralew', 'Synco']

all_clear = False
count = 0

table_list=[]

#repeatedly try to generate the font list document
#on errors, add the failing font to the list of ignores
while not all_clear:
    all_files = []
    #make the list of all files first
    for root,dirs,files in os.walk(fontpath):
        for f in files:
            all_files.append(os.path.join(root, f))

    all_files.sort()
    for f in all_files:
        if f[-4:] == '.ttf' and not re.search('/src/', f) and not re.search('\.hg', f) and not check_ignore(f, ignores):
            #p = Path(f)
            filename = os.path.basename(f)

            parts = os.path.splitext(filename)
            name_only = parts[0]
            
            print name_only

            #if count < 10:
            if True:
                try:
                    pdfmetrics.registerFont(TTFont(name_only, f))
                except:
                    pass
                    print "skipping: %s from: %s" % (name_only, f)
                else:
                    text1 = '<font name="%s" size="%s">%s</font>' % (name_only, sample_size, name_only)
                    text2 = '<font name="%s" size="%s">%s</font>' % (name_only, sample_size, sample_text)
                    # print text1, text2
                    row = [ Paragraph(text1, styles["Normal"]), Paragraph(text2, styles["Normal"]) ]
                    table_list.append(row)
            count += 1

    doc = SimpleDocTemplate("test.pdf",pagesize=letter,
                        rightMargin=36,leftMargin=36,
                        topMargin=36,bottomMargin=18)

    Story = [ Table(table_list, colWidths=(180,360)) ]

    try:
        doc.build(Story)
    except ValueError, result:
        print result
        parts = str(result).split('+')
        ignores.append(parts[1][:5])
        print ignores

    all_clear = True

        
