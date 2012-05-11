#!/usr/bin/python2.6

from datetime import date

import codecs
import fontforge
import json
import logging
import os
import sys

# This is only here to have the JSON file data written in a predictable way
# We only care about the the json object being able to iterate over the keys, so
# other stuff might be broken...
class InsertOrderedDict(dict):

  def __init__(self):
    dict.__init__(self)
    self.orderedKeys = []

  def __setitem__(self, key, item):
    dict.__setitem__(self, key, item)
    if key not in self.orderedKeys:
      self.orderedKeys.append(key)

  def __delitem__(self, key):
    dict.__delitem__(self, key)
    orderedKeys.remove(key)

  def clear(self):
    dict.clear(self)
    orderedKeys = []

  def copy(self):
    dictCopy = InsertOrderedDict()
    for key in self.orderedKeys:
      dictCopy[key] = dict.get(self, key)
    return dictCopy

  def keys(self):
    return self.orderedKeys

  def items(self):
    return [(key, dict.get(self, key)) for key in self.orderedKeys]

  def iteritems(self):
    return iter(self.items())

  def iterkeys(self):
    return iter(self.orderedKeys)

  # That's definitely a mess, but doing our best
  def update(self, dictionary=None, **kwargs):
    for key in dictionary.iterkeys():
      if key not in self.orderedKeys:
        self.orderedKeys.append(key)
    if len(kwargs):
      for key in kwargs:
        if key not in self.orderedKeys:
          self.orderedKeys.append(key)
    dict.update(self, dictionary, **kwargs)

  def pop(self, key, *args):
    self.orderedKeys.remove(key)
    return dict.pop(self, key, *args)

  def popitem(self):
    if self.orderedKeys:
      return self.pop(self.orderedKeys[0])
    return dict.popitem(self) # should raise KeyError

SUPPORTED_SUBSETS = frozenset([
    "menu",
    "arabic",
    "armenian",
    "balinese",
    "bengali",
    "burmese",
    "cherokee",
    "cyrillic",
    "cyrillic-ext",
    "ethiopic",
    "georgian",
    "greek",
    "greek-ext",
    "gujarati",
    "hebrew",
    "hindi",
    "japanese",
    "javanese",
    "kannada",
    "khmer",
    "korean",
    "lao",
    "latin",
    "latin-ext",
    "malayalam",
    "oriya",
    "osmanya",
    "sinhala",
    "tamil",
    "telugu",
    "thai",
    "tibetan",
    "vietnamese"
])

def usage():
  print >> sys.stderr, "genmetadata.py family_directory"

def inferLicense(familydir):
  if familydir.find("ufl/") != -1:
    return "UFL"
  if familydir.find("ofl/") != -1:
    return "OFL"
  if familydir.find("apache/") != -1:
    return "Apache2"
  return ""

def inferStyle(ffont):
  if ffont.italicangle == 0.0:
    return "normal"
  return "italic"

def inferFamilyName(familydir):
  files = os.listdir(familydir)
  for f in files:
    if f.endswith(".ttf"):
      filepath = os.path.join(familydir, f)
      ffont = fontforge.open(filepath)
      return ffont.familyname

def createFonts(familydir, familyname):
  fonts = []
  files = os.listdir(familydir)
  for f in files:
    if f.endswith(".ttf"):
      fontmetadata = InsertOrderedDict()
      filepath = os.path.join(familydir, f)
      ffont = fontforge.open(filepath)
      fontmetadata["name"] = familyname
      fontmetadata["style"] = inferStyle(ffont)
      fontmetadata["weight"] = ffont.os2_weight
      fontmetadata["filename"] = f
      fontmetadata["postScriptName"] = ffont.fontname
      fontmetadata["fullName"] = ffont.fullname
      fonts.append(fontmetadata)
  return fonts

def inferSubsets(familydir):
  subsets = set()
  files = os.listdir(familydir)
  for f in files:
    index = f.rfind(".")
    if index != -1:
      extension = f[index + 1:]
      if extension in SUPPORTED_SUBSETS:
        subsets.add(extension)
  if len(subsets) == 0:
    return ["latin"]
  return sorted(subsets)

def setIfNotPresent(metadata, key, value):
  if key not in metadata:
    metadata[key] = value

def genmetadata(familydir):
  metadata = InsertOrderedDict()
  if hasMetadata(familydir):
    metadata = loadMetadata(familydir)
  familyname = inferFamilyName(familydir)
  setIfNotPresent(metadata, "name", familyname)
  setIfNotPresent(metadata, "designer", "")
  setIfNotPresent(metadata, "license", inferLicense(familydir))
  setIfNotPresent(metadata, "visibility", "Internal")
  setIfNotPresent(metadata, "category", "")
  setIfNotPresent(metadata, "size", -1)
  setIfNotPresent(metadata, "dateAdded", getToday())
  metadata["fonts"] = createFonts(familydir, familyname)
  metadata["subsets"] = inferSubsets(familydir)
  return metadata

def getToday():
  return unicode(date.today().strftime("%Y-%m-%d"))

def hasMetadata(familydir):
  return os.path.exists(os.path.join(familydir, "METADATA.json"))

def loadMetadata(familydir):
  with codecs.open(os.path.join(familydir, "METADATA.json"), 'r', encoding="utf_8") as fp:
    return sortOldMetadata(json.load(fp))

def sortOldMetadata(oldmetadata):
  orderedMetadata = InsertOrderedDict()
  orderedMetadata["name"] = oldmetadata["name"]
  orderedMetadata["designer"] = oldmetadata["designer"]
  orderedMetadata["license"] = oldmetadata["license"]
  orderedMetadata["visibility"] = oldmetadata["visibility"]
  orderedMetadata["category"] = oldmetadata["category"]
  orderedMetadata["size"] = oldmetadata["size"]
  orderedMetadata["fonts"] = sortFont(oldmetadata["fonts"])
  orderedMetadata["subsets"] = sorted(oldmetadata["subsets"])
  orderedMetadata["dateAdded"] = oldmetadata["dateAdded"]
  return orderedMetadata

def sortFont(fonts):
  sortedfonts = []
  for font in fonts:
    fontMetadata = InsertOrderedDict()
    fontMetadata["name"] = font["name"]
    fontMetadata["style"] = font["style"]
    fontMetadata["weight"] = font["weight"]
    fontMetadata["filename"] = font["filename"]
    fontMetadata["postScriptName"] = font["postScriptName"]
    fontMetadata["fullName"] = font["fullName"]
    sortedfonts.append(fontMetadata)
  return sortedfonts

def striplines(jsontext):
  lines = jsontext.split("\n")
  newlines = []
  for line in lines:
    newlines.append("%s\n" % (line.rstrip()))
  return "".join(newlines)

def writeFile(familydir, metadata):
  filename = "METADATA.json"
  if hasMetadata(familydir):
    filename = "METADATA.json.new"
  with codecs.open(os.path.join(familydir, filename), 'w', encoding="utf_8") as f:
    f.write(striplines(json.dumps(metadata, indent=2, ensure_ascii=False)))

def run(familydir):
 writeFile(familydir, genmetadata(familydir))

def main(argv=None):
  if argv is None:
    argv = sys.argv
  if len(argv) != 2:
    usage()
    return 1
  run(argv[1])
  return 0

if __name__ == '__main__':
  sys.exit(main())
