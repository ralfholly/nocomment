# NoComment!
NoComment! is a little tool that counts lines in source code. As of now, only languages based on C syntax (C, C++, Java) are supported.
In order to avoid command-line overflow, NoComment reads the file names of the files to be processed from standard input.

## Examples
```
find -iname '*.[ch]' | nocomment.py
ls -1 *.c *.h *.java | nocomment.py
```

## Output
The following conventions and abbreviations are used:
* Physical lines (Phys): Equivalent to the number of '\n' characters in the file.
* Black lines (Black): Lines containing code, comments, or both.
* Comment lines (Comnt): Lines containing comments or parts of multi-line comments.
* White lines: Lines consisting only of whitespace.
* Comnt%: Total number of comment lines divided by total number of black lines (in percent).
