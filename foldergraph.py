#!/usr/bin/env python
# vim: set fileencoding=utf8 :
from __future__ import division

import igraph, os
import fglib as fg

dup_filename = "mybookfiles.txt"
file_filename = "files.txt"
ignore_fname = "ignore.txt"

g = fg.FolderGraph(file_filename, ignore_fname, dup_filename)
print g.summary()

g.simplify(combine_edges=sum)
print g.summary()
g.printout(95)
print "----------", int(g.tot_size/1024/1024/1024),"G" # len(out),

g.contract()
print g.summary()
g.simplify(combine_edges=sum)
print g.summary()
g.printout(50)
