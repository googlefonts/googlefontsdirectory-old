import fontforge

f = fontforge.open("Crimson-Roman.sfd")

chars = [
"zero",
"one",
"two",
"three",
"four",
"five",
"six",
"seven",
"eight",
"nine",

"exclam",
"percent",
"parenleft",
"parenright",
"plus",
"comma",
"hyphen",
"period",
"slash",

"colon",
"semicolon",
"less",
"equal",
"greater",
"question",

"a",
"b",
"c",
"d",
"e",
"egrave",
"f",
"g",
"h",
"i",
"j",
"k",
"l",
"m",
"n",
"o",
"p",
"q",
"r",
"s",
"t",
"u",
"v",
"w",
"x",
"y",
"z",

"A",
"B",
"C",
"D",
"E",
"Egrave",
"F",
"G",
"H",
"I",
"J",
"K",
"L",
"M",
"N",
"O",
"P",
"Q",
"R",
"S",
"T",
"U",
"V",
"W",
"X",
"Y",
"Z",

"bracketleft",
"backslash",
"bracketright",

"braceleft",
"bar",
"braceright",

"asciitilde",

"brokenbar",
"section",

"paragraph",
"dagger",
"daggerdbl",
"uni2016", #doubleverticalline
]

for char in chars:
    newChar = f.createChar(-1, char + ".ordn")
    newChar.build()
    if not newChar.isWorthOutputting():
        print char
        newChar.addReference(char)

for char in chars:
    newChar = f.createChar(-1, char + ".subs")
    newChar.build()
    if not newChar.isWorthOutputting():
        print char
        newChar.addReference(char)

for char in chars:
    newChar = f.createChar(-1, char + ".ssup")
    newChar.build()
    if not newChar.isWorthOutputting():
        print char
        newChar.addReference(char)

for char in chars:
    newChar = f.createChar(-1, char + ".sinf")
    newChar.build()
    if not newChar.isWorthOutputting():
        print char
        newChar.addReference(char)

f.save("Crimson-Roman.sfd")
