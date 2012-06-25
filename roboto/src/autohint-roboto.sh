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
