#!/usr/bin/env python
import igraph, os

filename = "/Users/anaraven/Desktop/mybookfiles.txt"

tree = {}
def join_nodes(nodes):
    for i in range(len(nodes)-1):
        src = tree.get(nodes[i], {})
        for j in range(i+1, len(nodes)):
            src[nodes[j]] = src.get(nodes[j], 0) + 1

nodes = []
for line in file(filename, "r"):
    if line.startswith("#"):
        continue
    duptype, iden, depth, size, device, inode, priority, name = line.strip().split(" ", 7)
    dirn = os.path.dirname(name)
    if duptype == "DUPTYPE_FIRST_OCCURRENCE":
        join_nodes(nodes)
        nodes = [name]
    else:
        nodes.append(name)

print len(tree.keys())
