#!/usr/bin/env python
# vim: set fileencoding=utf8 :
from __future__ import division

import igraph, os

dup_filename = "mybookfiles.txt"
file_filename = "files.txt"
ignore_fname = "ignore.txt"

g = igraph.Graph(directed=False)

def add_node(graph, node, nd, nf):
    try:
        v = graph.vs.find(node)
        v["nd"] += nd
        v["nf"] += nf
    except ValueError as e:
        graph.add_vertex(name=node, nd=nd, nf=nf)

def join_nodes(nodes):
    for i in range(len(nodes)-1):
        src = nodes[i]
        # add_node(g, src)
        for j in range(i+1, len(nodes)):
            dst = nodes[j]
            # add_node(g, dst)
            g.add_edge(src[0], dst[0], weight=src[1], count=1)

#NR = 0
for line in file(file_filename, "r"):
#    NR += 1
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

def add_pct(g, thr, out = []):
    for edge in g.es:
        e0, e1 = edge.tuple
        count = edge["count"]
        nf0 = g.vs["nf"][e0]
        nf1 = g.vs["nf"][e1]
        try:
            pct0 = int(count*1000/nf0)/10
        except ZeroDivisionError:
            print g.vs["name"][e0], nf0, nf1, count
            pct0 = 0
        try:
            pct1 = int(count*1000/nf1)/10
        except ZeroDivisionError:
            print g.vs["name"][e0], nf0, nf1, count
            pct1 = 0
        pct = max(pct0, pct1)
        if pct >= thr:
            out.append( (pct, g.vs["name"][e0], nf0, pct0,
                              g.vs["name"][e1], nf1, pct1, count) )
    return out

nodes = []
# NR = 0
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
        join_nodes(nodes)
        nodes = [ (dirn, int(size)) ]
    else:
        tot_size += int(size)
        nodes.append( (dirn, int(size)) )

g.simplify(combine_edges="sum")
# print g.summary()
out = add_pct(g, 95)

def contract(g):
    ng = igraph.Graph(directed=False)
    for vertex in g.vs:
        add_node(ng, os.path.dirname(vertex["name"]),
                 nd=vertex["nd"], nf=vertex["nf"])
    # print ng.summary()
    for edge in g.es:
        e0, e1 = edge.tuple
        ng.add_edge(os.path.dirname(g.vs["name"][e0]),
                    os.path.dirname(g.vs["name"][e1]),
                    weight=edge["weight"], count=edge["count"])
    # print ng.summary()
    ng.simplify(combine_edges="sum")
    return ng

g = contract(g)
# print g.summary()
out2 = add_pct(g, 95)

def comp_tuple(x,y):
    if(x[0]<y[0]):
        return -1
    if(x[0]==y[0]):
        return 0
    return 1

def printout(out):
    out.sort(comp_tuple)
    for o in out:
        pct, name0, nf0, pct0, name1, nf1, pct1, count = o
        print name0, nf0, count, pct0
        print name1, nf1, count, pct1, "\n"

#       print( "%5.1f\n%s\t%d\t%d\n%s\t%d\t%d\n" % (pct,
#             name0, nf0, pct0, name1, nf1, pct1) )

printout(out)
print "----------", len(out), int(tot_size/1024/1024/1024),"G"
printout(out2)
