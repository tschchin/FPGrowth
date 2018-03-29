# FPGrowth.py
from collections import Counter
from FPTree import FPTree
from itertools import combinations
import math

def decimal_round(num):
    t = num * 100000
    t = math.floor(t)
    if t%10 >= 5:
        t+=10
    return "{:.4f}".format(math.floor(t/10)/10000)

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
        print('Item','\t','Freq','\t'+'Parent')
        for i in self.header:
            print(i,'\t',self.header[i]['freq'],end='\t')
            t = self.header[i]['head']
            #print(t)
            while t:
                print(str(t.parent),end="->")
                t = t.next_node
            print('NULL')

class FPGrowth():
    def __init__(self, min_sup,items):
        min_sup = float(min_sup)*len(items)
        f_dict = self.build_fp_dict(items) # frequent items dict

        # update f_list and items by min_sup
        del_key = self.get_key_under_minsup(f_dict,min_sup)
        for i in del_key:
            del f_dict[i]
        for item in items:
            for i in del_key:
                if i in item:
                    item.remove(i)
        freq_items = self.frequent_items(items,f_dict) # list

        header_table = HeaderTable(f_dict)
        FP_tree = FPTree()
        FP_tree.add_fp_set(freq_items)

        header_table.set_head(FP_tree)

        cond_pattern_base = self.build_cond_pattern_base(header_table.header)
        frequent_patterns = self.frequent_pattern_generate(cond_pattern_base)
        frequent_patterns.update(f_dict)

        self.fp = dict()
        for i in frequent_patterns:
            if frequent_patterns[i] >= min_sup:
                t = sorted(list(map(int,i.split(','))))
                t = list(map(str,t))
                key = ','.join(t)
                self.fp[key] = decimal_round(frequent_patterns[i]/len(items))
        self.fp = sorted(self.fp.items(),key=lambda key: (len(key[0].split(',')),list(map(int,key[0].split(',')))))

    def print_pattern(self,pats,min_sup):
        print("min_sup:",min_sup)
        ide = 1
        for i in pats:
            if pats[i]>=min_sup and len(i)==3:
                print(ide,i,pats[i])
                ide+=1

    def build_fp_dict(self,items):
        counter = Counter()
        for item in items:
            counter += Counter(item)
        f_list = counter.most_common() # sort counter -> list
        return dict(f_list)

    def get_key_under_minsup(self,f_dict,min_sup):
        del_key = []
        for i in f_dict:
            if f_dict[i] < min_sup:
                del_key.append(i)
        return del_key

    def frequent_items(self,items,f_dict):
        '''
            order items(data) by f_list(f_dict)
        '''
        freq_items = []
        for item in items:
            temp = sorted(item,key = lambda x: -f_dict[x])
            freq_items.append(temp)
        return freq_items

    def build_cond_pattern_base(self,header):
        cond_pattern_base = dict()
        for pattern in header:
            next_node = item = header[pattern]['head']
            #pattern_base[str(item)] = dict()
            t = dict()
            while next_node is not None:
                pattern_base = self.get_pattern_base(next_node)
                if pattern_base[0] is not "":
                    t[pattern_base[0]] = pattern_base[1]
                next_node = next_node.next_node
            if t != {}:
                cond_pattern_base[str(item)] = t
        return cond_pattern_base

    def get_pattern_base(self,node):
        pattern_len = len(str(node))
        pattern_base = ""
        pattern_count = node.count
        while node.parent is not None:
            pattern_base = str(node)+','+pattern_base
            node = node.parent
        return (pattern_base[:-(pattern_len+2)],pattern_count)

    def frequent_pattern_generate(self,fpb):
        total_fp = dict()
        for pbs in fpb:
            for pb in fpb[pbs]:
                for i in range(len(pb)):
                    for fp_comb in combinations(pb.split(','),i+1):
                        t = ','.join(fp_comb)
                        key = t+','+pbs
                        if key in total_fp:
                            total_fp[key] += fpb[pbs][pb]
                        else:
                            total_fp[key] = fpb[pbs][pb]
        return total_fp

    def outcome(self,min_sup,header_table):
        print('MIN_SUPPORT:',min_sup)
        print('HEADER TABLE:')
        header_table.print_header_table()
