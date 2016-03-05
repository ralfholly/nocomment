#! /usr/bin/env python

import sys
import re

VERSION = "0.0.1"

RE_BLANK_LINE = re.compile(r"\s*\n")
RE_MULTI_COMMENT_SINGLE_LINE = re.compile(r".*/\*.*\*/")
RE_MULTI_COMMENT_BEGIN = re.compile(r".*/\*")
RE_MULTI_COMMENT_END = re.compile(r".*\*/")
RE_SINGLE_COMMENT = re.compile(r".*//.*")

FORMAT_ABSOLUTE_TITLE_STR  = "{_pl:>8s}  {_bl:>8s}  {_cl:>8s}  {_clp:>8s}      {_fn}"
FORMAT_ABSOLUTE_STR = "{_pl:>8d}  {_bl:>8d}  {_cl:>8d}  {_clp:>8.0f}      {_fn}"

gOptPure = False

def show_copyright():
    print "Copyright 2010 by Ralf Holly."
    print ""
    print "This program is free software: you can redistribute it and/or modify"
    print "it under the terms of the GNU General Public License as published by"
    print "the Free Software Foundation, either version 3 of the License, or"
    print "(at your option) any later version."
    print ""
    print "This program is distributed in the hope that it will be useful,"
    print "but WITHOUT ANY WARRANTY; without even the implied warranty of"
    print "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
    print "GNU General Public License for more details."
    print ""
    print "You should have received a copy of the GNU General Public License"
    print "along with this program.  If not, see <http://www.gnu.org/licenses/>."

def process_file(filename):

    physicalLines = blackLines = whiteLines = commentLines = 0
    waitForCommentEnd = False

    file = None
    try:
        file = open(filename, "r")

        for line in file:
            physicalLines += 1

            # If only whitespace.
            if re.match(RE_BLANK_LINE, line):
                whiteLines += 1
                continue

            # Otherwise we have code or comments.
            blackLines += 1

            # If waiting for a */
            if waitForCommentEnd:
                commentLines += 1
                if re.match(RE_MULTI_COMMENT_END, line):
                    waitForCommentEnd = False
                else:
                    continue
                    
            # If /* ... */ on single line.
            if re.match(RE_MULTI_COMMENT_SINGLE_LINE, line):
                commentLines += 1

            # If /* ... not closed on same line.
            elif re.match(RE_MULTI_COMMENT_BEGIN, line):
                commentLines += 1
                waitForCommentEnd = True
                continue

            # If // comment
            elif re.match(RE_SINGLE_COMMENT, line):
                commentLines += 1

    except IOError:
        return None

    finally:
        if file: file.close()

    return (filename, physicalLines, blackLines, commentLines, whiteLines)

def handle_args():
    global gOptPure

    if len(sys.argv) == 2:
        arg1 = sys.argv[1]
        if arg1 in ('-h', '--help'):
            print "Usage: nocomment.py [arg]"
            print "    -h, --help          This help message"
            print "    -v, --version       Version information"
            print "    -p, --pure          Leaves out header and footer"
            print "Without arguments, reads a list of files to be analyzed from standard input."
            sys.exit(0)
        elif arg1 in ('-v', '--version'):
            print "NoComment! Version {version}".format(version=VERSION)
            print ""
            show_copyright()
            sys.exit(0)
        elif arg1 in ('-p', '--pure'):
            gOptPure = True
        else:
            print "Unknown command-line option."
            sys.exit(1)

def main():
    
    handle_args()

    if not gOptPure:
        print FORMAT_ABSOLUTE_TITLE_STR.format(_pl="Phys", _bl="Black", _cl="Comnt",
            _clp="Comnt%", _fn="File")

    totalPhysical = 0
    totalBlack = 0
    totalComment = 0
    totalWhite = 0

    try:
        while True:
            f = raw_input()

            result = process_file(f)

            if result:
                fn, pl, bl, cl, wl = result
                totalPhysical += pl
                totalBlack += bl
                totalComment += cl
                totalWhite +=wl

                clp = 100.0 * cl / bl if bl > 0 else 0
                print FORMAT_ABSOLUTE_STR.format(_pl=pl, _bl=bl, _cl=cl, _clp=clp, _fn=fn)
            else:
                print >> sys.stderr, "File access error: {0}".format(f)
    except EOFError:
        pass

    except KeyboardInterrupt:
        sys.exit(1)

    if not gOptPure:
        totalClp = 100.0 * totalComment / totalBlack if totalBlack > 0 else 0
        print FORMAT_ABSOLUTE_STR.format(_pl=totalPhysical, _bl=totalBlack, _cl=totalComment,
            _clp=totalClp, _fn="SUMMARY")

main()



