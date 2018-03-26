# FPTree.py

class Node():
    def __init__(self,info,parent=None):
        self.info = info    # pattern name
        self.count = 1      # frequency count
        self.child = []
        self.next_node = None   # next same frequent pattern
        self.parent = parent
    def __str__(self):
        return str(self.info) #return as string

class FPTree():
    def __init__(self):
        self.root = Node(None)

    def create(self,fp):
        self.root.child.append(fp)

    def add_fp_set(self, fp_set):
        for fp in fp_set:
            cur_node = self.root
            childs = cur_node.child
            for p in fp:
                if len(childs)==0:  # child is empty => pattern add to child directly
                    node = Node(p,cur_node)
                    cur_node = node
                    childs.append(node)
                    childs = node.child
                else:
                    it = iter(childs)
                    while True:
                        try:   # there is pattern => add freqency(count)
                            child = next(it)
                            if child.info==p:
                                child.count += 1
                                cur_node = child
                                childs = child.child
                                add = 0
                                break
                        except StopIteration:   # pattern haven't in the child
                                node = Node(p,cur_node)  # add pattern to child
                                cur_node = node
                                childs.append(node)
                                childs = node.child
                                break

    def deep_first(self,node):
        yield node  # return self node
        if len(node.child):
            for i in node.child:
                yield from self.deep_first(i) # deep to child node
