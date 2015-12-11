#!/usr/bin/env python
# vim: set fileencoding=utf8 :
from __future__ import division

import igraph, os

folder = "/Users/anaraven/Src/FolderDups/"
dup_filename = folder + "mybookfiles.txt"
file_filename = folder + "files.txt"
ignore_fname = "ignore.txt"

g = igraph.Graph(directed=False)

def add_node(graph, node, nd=0, nf=0):
    try:
        graph.vs.find(node)
    except ValueError as e:
        graph.add_vertex(name=node, nd=nd, nf=nf)

def join_nodes(nodes):
    for i in range(len(nodes)-1):
        src = nodes[i]
        # add_node(g, src)
        for j in range(i+1, len(nodes)):
            dst = nodes[j]
            # add_node(g, dst)
            g.add_edge(src, dst, weight=1)

NR = 0
for line in file(file_filename, "r"):
    NR += 1
#    if NR % 500==0:
#        print NR
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
NR = 0
tot_size = 0
for line in file(dup_filename, "r"):
    if line.startswith("#"):
        continue
    if should_ignore(line):
        continue
    duptype, iden, depth, size, device, inode, priority, name = line.strip().split(" ", 7)
    if int(size)<1000000:
        continue
    dirn = os.path.dirname(name)
    if duptype == "DUPTYPE_FIRST_OCCURRENCE":
        NR += 1
        join_nodes(nodes)
        nodes = [dirn]
#        if NR % 100==0:
#            print NR
    else:
        tot_size += int(size)
        nodes.append(dirn)

g.simplify(combine_edges=sum)
# print g.summary()

def gen_tuple(e0, e1):
    try:
        eid = g.get_eid(e0, e1)
    except igraph._igraph.InternalError as e:
        eid = g.get_eid(e1, e0)
    weight = g.es["weight"][eid]
    nf0 = g.vs["nf"][e0]
    nf1 = g.vs["nf"][e1]
    pct0 = int(weight*1000/nf0)/10
    pct1 = int(weight*1000/nf1)/10
    pct = max(pct0, pct1)
    return (pct, g.vs["name"][e0], nf0, pct0, g.vs["name"][e1], nf1, pct1)

comps = g.components()
out = []
for el in comps:
    if len(el)==1:
        continue
    for i in range(len(el)-1):
        for j in range(i+1, len(el)):
            try:
                o = gen_tuple(el[i], el[j])
            except igraph._igraph.InternalError as e:
                continue
            if o[0]>=80.0:
                out.append( o )

def comp_tuple(x,y):
    if(x[0]<y[0]):
        return -1
    if(x[0]==y[0]):
        return 0
    return 1

out.sort(comp_tuple)

for o in out:
    print o[1], o[2], o[3]
    print o[4], o[5], o[6], "\n"

print len(out), int(tot_size/1024/1024/1024),"G"
