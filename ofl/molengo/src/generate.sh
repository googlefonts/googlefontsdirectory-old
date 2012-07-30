#!/bin/sh

# $Id: generate.sh 1885 2007-06-08 00:01:59Z remyoudompheng $

set -e 

test -d generated || mkdir generated
#./ttpostproc.pl generated/*.ttf
xgridfit xgf/Molengo-Regular.xgf && fontforge -script Molengo-Regular.pe 
./generate.pe *.ttf
#rm *.ttf
