#!/usr/bin/env python
# vim: set fileencoding=utf8 :

import igraph, os

filename = "/Users/anaraven/Desktop/mybookfiles.txt"

g = igraph.Graph()

def add_node(graph, node):
    try:
        graph.vs.find(node)
    except ValueError as e:
        graph.add_vertex(node)

def join_nodes(nodes):
    for i in range(len(nodes)-1):
        src = nodes[i]
        add_node(g, src)
        for j in range(i+1, len(nodes)):
            dst = nodes[j]
            add_node(g, dst)
            g.add_edge(src, dst, weight=1)

nodes = []
NR = 0
tot_size = 0
for line in file(filename, "r"):
    if line.startswith("#"):
        continue
    if line.find("Public/Shared Videos/Música")>=0:
        continue
    duptype, iden, depth, size, device, inode, priority, name = line.strip().split(" ", 7)
    if int(size)<10000000:
        continue
    dirn = os.path.dirname(name)
    if duptype == "DUPTYPE_FIRST_OCCURRENCE":
        NR += 1
        join_nodes(nodes)
        nodes = [dirn]
        if NR % 100==0:
            print NR
    else:
        tot_size += int(size)
        nodes.append(dirn)

g.simplify(combine_edges=sum)
print g.summary()
print g.components()
print int(tot_size/1024/1024/1024),"G"
