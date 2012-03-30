#! /bin/sh
# Copyright (c) Werner Lemberg, published under CC-0
#
# autohint.sh
#
# This script calls ttfautohint and ttx to autohint a set of fonts.  Please
# adjust the parameters of ttfautohint as needed for your purposes.
#
# Example call:
#
#   sh autohint.sh *.ttf
#
# This script appends `-TA' to the output font name.  For example, input
# file `bar.ttf' is converted to `bar-TA.ttf'.
#
# The `--hinting-limit' option is available since ttfautohint version 0.8.

for i; do
  infile=`basename $i`
  outfile=`echo $infile | sed 's/.ttf/-TA.ttf/'`
  ttxfile=`echo $outfile | sed 's/.ttf/.ttx/'`

  echo $infile

  ttfautohint --verbose \
              --increase-x-height \
              --hinting-range-min=8 \
              --hinting-range-max=50 \
              --hinting-limit=200 \
              $i $outfile

  rm -f $ttxfile
  ttx $outfile
  rm $outfile
  ttx $ttxfile
  rm $ttxfile
done
