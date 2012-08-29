#!/bin/sh

cd $(dirname "${BASH_SOURCE[0]}")
DIRECTORIES=""

for metadata in $(find ../../{ofl,ufl,apache} -name METADATA.json); do
  DIRECTORIES="$DIRECTORIES $(dirname $metadata)"
done

ant lint-jar

java -jar dist/lint.jar $DIRECTORIES

cd - > /dev/null
