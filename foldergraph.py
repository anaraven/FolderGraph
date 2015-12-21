#!/usr/bin/env python
# vim: set fileencoding=utf8 :
from __future__ import division

import igraph, os
import fglib as fg

dup_filename = "mybookfiles.txt"
file_filename = "files.txt"
ignore_fname = "ignore.txt"

ignored = fg.Ignored(ignore_fname)

g = igraph.Graph(directed=False)

for line in file(file_filename, "r"):
    if line.startswith("#"):
        continue
    if ignored.matches(line):
        continue
    name, d, f = line.strip().split("\t")
    g.add_vertex(name, nd=int(d), nf=int(f))

nodes = []
tot_size = 0
for line in file(dup_filename, "r"):
    if line.startswith("#"):
        continue
    if ignored.matches(line):
        continue
    duptype, iden, depth, size, device, inode, priority, name = line.strip().split(" ", 7)
    if int(size)<1e8:
        continue
    dirn = os.path.dirname(name)
    if duptype == "DUPTYPE_FIRST_OCCURRENCE":
        fg.join_nodes(g, nodes)
        nodes = [ (dirn, int(size)) ]
    else:
        tot_size += int(size)
        nodes.append( (dirn, int(size)) )
fg.join_nodes(g, nodes)

g.simplify(combine_edges=sum)
print g.summary()
# out = fg.add_pct(g, 95)
# fg.printout(out)
# print "----------", len(out), int(tot_size/1024/1024/1024),"G"

fg.contract(g)
print g.summary()
g.simplify(combine_edges=sum)
print g.summary()
out2 = fg.add_pct(g, 50)
fg.printout(out2)
