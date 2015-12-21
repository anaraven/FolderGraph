#!/usr/bin/env python
# vim: set fileencoding=utf8 :
from __future__ import division

import igraph, os
import fglib as fg

dup_filename = "mybookfiles.txt"
file_filename = "files.txt"
ignore_fname = "ignore.txt"

g = fg.FolderGraph(file_filename, ignore_fname, dup_filename,1e6)
g.simplify(combine_edges=sum)
print g.summary()
g.printout(95)

g.contract()
g.simplify(combine_edges=sum)
print g.summary()
g.printout(90)

g.contract()
g.simplify(combine_edges=sum)
print g.summary()
g.printout(90)

g.contract()
g.simplify(combine_edges=sum)
print g.summary()
g.printout(90)


## next step: find unmatched files
