#!/usr/bin/env python
# vim: set fileencoding=utf8 :
from __future__ import division

import igraph, os
import fglib as fg

dup_filename = "mybookfiles.txt"
file_filename = "files.txt"
ignore_fname = "ignore.txt"

g = igraph.Graph(directed=False)

for line in file(file_filename, "r"):
    name, d, f = line.strip().split("\t")
    g.add_vertex(name, nd=int(d), nf=int(f))

ignore = []
for line in file(ignore_fname, "r"):
    ignore.append(line.strip())

def should_ignore(line):
    for patrn in ignore:
        if line.find(patrn)>=0:
            return True
    return False

nodes = []
tot_size = 0
for line in file(dup_filename, "r"):
    if line.startswith("#"):
        continue
    if should_ignore(line):
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
g.simplify(combine_edges="sum")
print g.summary()
out = fg.add_pct(g, 95)
fg.printout(out)
print "----------", len(out), int(tot_size/1024/1024/1024),"G"

g2 = fg.contract(g)
print g2.summary()
out2 = fg.add_pct(g2, 95)
fg.printout(out2)
