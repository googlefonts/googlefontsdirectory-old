import sys

glyphname = sys.argv[1]
glyphix = ord(glyphname)
fi = file('/tmp/foo.ps')
fo = file('/tmp/foo.sfd', 'w')

print >> fo, 'SplineFontDB: 1.0'
print >> fo, 'FontName: foo'
print >> fo, 'FullName: foo'
print >> fo, 'FamilyName: foo'
print >> fo, 'Ascent: 800'
print >> fo, 'Descent: 200'
print >> fo, 'Encoding: iso8859_1'
print >> fo, 'UnicodeInterp: none'
print >> fo, 'BeginChars: 256 1'
print >> fo, 'StartChar:', glyphname
print >> fo, 'Encoding:', glyphix, glyphix, 0
print >> fo, 'Width: 600'
print >> fo, 'Flags: O'
print >> fo, 'Fore'
for l in fi.xreadlines():
    ls = l.split()
    if ls[-1] in ('c', 'm', 'l'):
        new = []
        for i in range(len(ls) - 1):
            coord = float(ls[i])
            if i % 2: coord = 800 - coord
            new.append('%g' % coord)
        print >> fo, ' '.join(new), ls[-1], 0
print >> fo, 'EndSplineSet'
print >> fo, 'EndChar'
print >> fo, 'EndChars'
print >> fo, 'EndSplineFont'
