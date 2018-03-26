# FPGrowth.py
from collections import Counter
from FPTree import FPTree

class HeaderTable():
    def __init__(self,f_dict):
        self.header = dict()
        for i in f_dict:
            self.header[i] = {'freq':f_dict[i],'head':None}
        #for i in f_dict:
        #    print(self.header['0']['head'])
    def set_head(self,FP_tree):
        nodes = FP_tree.deep_first(FP_tree.root)
        #header = self.header
        for node in nodes:
            #print(type(node),node)
            if node.info is not None:
                #print(node)
                if self.header[node.info]['head'] is None:
                    self.header[node.info]['head'] = node
                else:
                    next_node = self.header[node.info]['head']
                    while next_node:
                        t = next_node
                        next_node = next_node.next_node
                    t.next_node = node
    def print_header_table(self):
        print('Item','\t','Freq','\t'+'Node:Count')
        for i in self.header:
            print(i,'\t',self.header[i]['freq'],end='\t')
            t = self.header[i]['head']
            #print(t)
            while t:
                print(str(t)+':'+str(t.count),end="->")
                t = t.next_node
            print('NULL')

class FPGrowth():
    def __init__(self, min_sup,items):
        self.min_sup = min_sup
        self.f_dict = self.build_f_dict(items) # dict
        self.freq_items = self.frequent_items(items) # list
        header_table = HeaderTable(self.f_dict)
        FP_tree = FPTree()
        FP_tree.add_fp_set(self.freq_items)

        header_table.set_head(FP_tree)

        header_table.print_header_table() # print header file

        t = FP_tree.deep_first(FP_tree.root) # print fp_tree by deep_first
        for i in t:
            print(i,i.parent)


    def build_f_dict(self,items):
        counter = Counter()
        for item in items:
            counter += Counter(item)
        f_list = counter.most_common() # sort counter -> list
        return dict(f_list)

    def frequent_items(self,items):
        freq_items = []
        for item in items:
            temp = sorted(item,key = lambda x: -self.f_dict[x])
            freq_items.append(temp)
        return freq_items
