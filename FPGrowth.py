# FPGrowth.py
from collections import Counter
from FPTree import FPTree

class FPGrowth():
    def __init__(self, min_sup,items):
        self.min_sup = min_sup
        #self.items = items
        self.f_list = self.build_f_list(items) # dict
        self.freq_items = self.frequent_items(items) # list
        #print(self.f_list)
        #print(self.freq_items)
        self.FPTree = FPTree()
        self.FPTree.add_fp_set(self.freq_items)
        t = self.FPTree.deep_first(self.FPTree.root)
        for i in t:
            print(i,i.count)

    def build_f_list(self,items):
        counter = Counter()
        for item in items:
            counter += Counter(item)
        f_list = counter.most_common() # sort counter -> list
        return dict(f_list)

    def frequent_items(self,items):
        freq_items = []
        for item in items:
            temp = sorted(item,key = lambda x: -self.f_list[x])
            freq_items.append(temp)
        return freq_items
