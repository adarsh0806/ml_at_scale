#!/usr/bin/env python

import sys

for line in sys.stdin:
    print "chars", len(line.rstrip('\n'))
    print "words", len(line.split())
    print "lines", 1
    