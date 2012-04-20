#!/usr/bin/python2.6

from UserDict import IterableUserDict
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

def genmetadata(familydir):
  metadata = InsertOrderedDict()
  familyname = inferFamilyName(familydir)
  metadata["name"] = familyname
  metadata["designer"] = ""
  metadata["license"] = inferLicense(familydir)
  metadata["visibility"] = "Internal"
  metadata["category"] = ""
  metadata["size"] = -1
  metadata["fonts"] = createFonts(familydir, familyname)
  metadata["subsets"] = inferSubsets(familydir)
#  if hasMetadata(familydir):
#    oldmetadata = loadMetadata(familydir)
#  diff = set(metadata["subsets"]).difference(set(oldmetadata["subsets"]))
#  if diff:
#    oldmetadata["subsets"].extend([subset for subset in diff])
#    writeOldMetadata(familydir, oldmetadata)
  return metadata

#def hasMetadata(familydir):
#  return os.path.exists(os.path.join(familydir, "METADATA.json"))

#def loadMetadata(familydir):
#  with open(os.path.join(familydir, "METADATA.json"), 'r') as fp:
#    return json.load(fp)

#def sortFont(fonts):
#  sortedfonts = []
#  for font in fonts:
#    metadatafont = InsertOrderedDict()
#    metadatafont["name"] = font["name"]
#    metadatafont["style"] = font["style"]
#    metadatafont["weight"] = font["weight"]
#    metadatafont["filename"] = font["filename"]
#    metadatafont["postScriptName"] = font["postScriptName"]
#    metadatafont["fullName"] = font["fullName"]
#    sortedfonts.append(metadatafont)
#  return sortedfonts

def striplines(jsontext):
  lines = jsontext.split("\n")
  newlines = []
  for line in lines:
    newlines.append(line.rstrip())
  return "\n".join(newlines)

#def writeOldMetadata(familydir, oldmetadata):
#  metadataToWrite = InsertOrderedDict()
#  metadataToWrite["name"] = oldmetadata["name"]
#  metadataToWrite["designer"] = oldmetadata["designer"]
#  metadataToWrite["license"] = oldmetadata["license"]
#  metadataToWrite["visibility"] = oldmetadata["visibility"]
#  metadataToWrite["category"] = oldmetadata["category"]
#  metadataToWrite["size"] = oldmetadata["size"]
#  metadataToWrite["fonts"] = sortFont(oldmetadata["fonts"])
#  metadataToWrite["subsets"] = sorted(oldmetadata["subsets"])
#  print json.dumps(metadataToWrite, indent=2)

def writeFile(familydir, metadata):
  with open(os.path.join(familydir, "METADATA.json"), 'w') as f:
    f.write(striplines(json.dumps(metadata, indent=2)))

def run(familydir):
 writeFile(familydir, genmetadata(familydir))

# TODO: clean up code and enable overwriting of existing METADATA.json files
# for update.
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
