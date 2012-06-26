#! /bin/sh
# Copyright (c) Werner Lemberg, published under CC-0
#
# autohint.sh
#
# This script calls ttfautohint 0.9 and ttx to auto-hint a set of fonts. 
# Please adjust the parameters of ttfautohint as needed for your purposes.
#
# Example call:
#
#   sh autohint.sh *.ttf
#
# This script appends `-TA' to the output font name.  For example, input
# file `bar.ttf' is converted to `bar-TA.ttf'.
#
# Since the old Roboto values are now the default, it has
# become much simpler

ttfautohint --verbose -f Roboto-Black.ttf Roboto-Black-TA.ttf;
ttfautohint --verbose -f Roboto-BlackItalic.ttf Roboto-BlackItalic-TA.ttf;
ttfautohint --verbose -f Roboto-Bold.ttf Roboto-Bold-TA.ttf;
ttfautohint --verbose -f Roboto-BoldItalic.ttf Roboto-BoldItalic-TA.ttf;
ttfautohint --verbose -f Roboto-Italic.ttf Roboto-Italic-TA.ttf;
ttfautohint --verbose -f Roboto-Light.ttf Roboto-Light-TA.ttf;
ttfautohint --verbose -f Roboto-LightItalic.ttf Roboto-LightItalic-TA.ttf;
ttfautohint --verbose -f Roboto-Medium.ttf Roboto-Medium-TA.ttf;
ttfautohint --verbose -f Roboto-MediumItalic.ttf Roboto-MediumItalic-TA.ttf;
ttfautohint --verbose -f Roboto-Regular.ttf Roboto-Regular-TA.ttf;
ttfautohint --verbose -f Roboto-Thin.ttf Roboto-Thin-TA.ttf;
ttfautohint --verbose -f Roboto-ThinItalic.ttf Roboto-ThinItalic-TA.ttf;
ttfautohint --verbose -f RobotoCondensed-Bold.ttf RobotoCondensed-Bold-TA.ttf;
ttfautohint --verbose -f RobotoCondensed-BoldItalic.ttf RobotoCondensed-BoldItalic-TA.ttf;
ttfautohint --verbose -f RobotoCondensed-Italic.ttf RobotoCondensed-Italic-TA.ttf;
ttfautohint --verbose -f RobotoCondensed-Light.ttf RobotoCondensed-Light-TA.ttf;
ttfautohint --verbose -f RobotoCondensed-LightItalic.ttf RobotoCondensed-LightItalic-TA.ttf;
ttfautohint --verbose -f RobotoCondensed-Regular.ttf RobotoCondensed-Regular-TA.ttf;

for i; do
  infile=`basename $i`
  outfile=`echo $infile | sed 's/.ttf/-TA.ttf/'`
  ttxfile=`echo $outfile | sed 's/.ttf/.ttx/'`

  echo $infile

  ttfautohint --verbose \
              $i $outfile

  rm -f $ttxfile
  ttx $outfile
  rm $outfile
  ttx $ttxfile
  rm $ttxfile
done

