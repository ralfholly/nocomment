#!/bin/sh

# Performs a simple regression test by comparing
# the results of a test run on some sample files
# in test/ to a file containing reference output

exit_code=0

cd test

find \
    -iname '*.[ch]' -o \
    -iname '*.[ch]pp' -o \
    -iname '*.java' \
    | sort \
    | ../nocomment.py > output

diff output output.ref
if [ $? -ne 0 ]; then exit_code=1; fi

cd ..

exit $exit_code
    
