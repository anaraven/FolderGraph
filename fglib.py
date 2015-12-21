
import igraph, os

class FolderGraph(igraph.Graph):
  def __init__(self, file_filename, ignore_fname, dup_filename, thr=1e8):
    super(FolderGraph, self).__init__(directed=False)
    ignored = Ignored(ignore_fname)

    for line in file(file_filename, "r"):
        if line.startswith("#"):
            continue
        if ignored.matches(line):
            continue
        name, d, f = line.strip().split("\t")
        self.add_vertex(name, nd=int(d), nf=int(f))

    nodes = []
    for line in file(dup_filename, "r"):
        if line.startswith("#"):
            continue
        if ignored.matches(line):
            continue
        duptype, iden, depth, size, device, inode, priority, name = line.strip().split(" ", 7)
        if int(size)<thr:
            continue
        dirn = os.path.dirname(name)
        if duptype == "DUPTYPE_FIRST_OCCURRENCE":
            self.join_nodes(nodes)
            nodes = [ (dirn, int(size)) ]
        else:
            nodes.append( (dirn, int(size)) )
    self.join_nodes(nodes)

  def add_node(self, node, nd, nf):
      try:
          v = self.vs.find(node)
          v["nd"] += nd
          v["nf"] += nf
      except ValueError as e:
          self.add_vertex(name=node, nd=nd, nf=nf)

  def join_nodes(self, nodes):
      for i in range(len(nodes)-1):
          src = nodes[i]
          for j in range(i+1, len(nodes)):
              dst = nodes[j]
              self.add_edge(src[0], dst[0], weight=src[1], count=1)

  def printout(self, thr):
    out=[]
    tot_size=0
    for edge in self.es:
      e0, e1 = edge.tuple
      count = edge["count"]
      nf0 = self.vs["nf"][e0]
      nf1 = self.vs["nf"][e1]
      try:
        pct0 = int(count*1000/nf0)/10
      except ZeroDivisionError:
        print self.vs["name"][e0], nf0, nf1, count
        pct0 = 0
      try:
        pct1 = int(count*1000/nf1)/10
      except ZeroDivisionError:
        print self.vs["name"][e0], nf0, nf1, count
        pct1 = 0
      pct = max(pct0, pct1)
      if pct >= thr:
        tot_size += edge["weight"]
        out.append( (pct, self.vs["name"][e0], nf0, pct0,
                          self.vs["name"][e1], nf1, pct1, count) )

    def comp_tuple(x,y):
      if(x[0]<y[0]):
          return -1
      if(x[0]==y[0]):
          return 0
      return 1

    out.sort(comp_tuple)
    for o in out:
      pct, name0, nf0, pct0, name1, nf1, pct1, count = o
      print name0, count, nf0, pct0, "%"
      print name1, count, nf1, pct1, "%\n"
#     print( "%5.1f\n%s\t%d\t%d\n%s\t%d\t%d\n" % (pct,
#             name0, nf0, pct0, name1, nf1, pct1) )
    print "---------- %d %dG" %(len(out), int(tot_size/1024/1024/1024))


  def contract(self):
    a = {x:os.path.dirname(x) for x in self.vs["name"]} #  name of ancestors of each node
    b = {x:1 for x in a.values()}.keys() #  list of internal nodes names
    c = dict(zip(b, range(len(b)))) # new numbers for internal nodes
    def y(x):
      if c.has_key(x):
        return c[x]
      else:
        return c[a[x]]
    self.contract_vertices([y(x) for x in self.vs["name"]],
        combine_attrs={"name":None, "nf":sum, "nd":sum})#  {"name":"first", "nf":"sum", "nd":"sum"})
    self.vs["name"] = b


class Ignored(object):
  def __init__(self, ignore_fname):
    self.ignore = []
    for line in file(ignore_fname, "r"):
        self.ignore.append(line.strip())

  def matches(self, line):
      for patrn in self.ignore:
          if line.find(patrn)>=0:
              return True
      return False
