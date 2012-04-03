#!/usr/bin/python

# Copyright 2010, Google Inc.
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
# bbox.py: A FontForge python script for printing bounding boxes
# to stdout in this format:
#
#   glyphname xmin ymin xmax ymax
#
# Usage:
#
#   $ python bbox.py Font.ttf 2> /dev/null
#   A 42.0 -32.0 782.0 1440.0
#   B 46.0 -72.0 752.0 1478.0
#   C 53.0 -26.0 821.0 1442.0
#   D 77.0 -26.0 773.0 1442.0

import fontforge, sys

def main(argv):
    font_in = argv[0]
    font = fontforge.open(font_in)
    for g in fontforge.activeFont().glyphs():
        bbox = g.boundingBox()
        print str(g.glyphname),
        print str(bbox[0]),
        print str(bbox[1]),
        print str(bbox[2]),
        print str(bbox[3])

if __name__ == '__main__':
    main(sys.argv[1:2])
