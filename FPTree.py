# FPTree.py

class Node():
    def __init__(self,info):
        self.info = info    # pattern name
        self.count = 1      # frequency count
        self.child = []
    def __str__(self):
        return str(self.info) #return as string

class FPTree():
    def __init__(self):
        self.root = Node(None)

    def create(self,fp):
        self.root.child.append(fp)

    def add_fp_set(self, fp_set):
        for fp in fp_set:
            childs = self.root.child
            for p in fp:
                if len(childs)==0:  # child is empty => pattern add to child directly
                    node = Node(p)
                    childs.append(node)
                    childs = node.child
                else:
                    it = iter(childs)
                    while True:
                        try:   # there is pattern => add freqency(count)
                            child = next(it)
                            if child.info==p:
                                child.count += 1
                                childs = child.child
                                add = 0
                                break
                        except StopIteration:   # pattern haven't in the child
                                node = Node(p)  # add pattern to child
                                childs.append(node)
                                childs = node.child
                                break

    def deep_first(self,node):
        yield node  # return self node
        if len(node.child):
            for i in node.child:
                yield from self.deep_first(i) # deep to child node
