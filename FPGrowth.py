# FPGrowth.py
from collections import Counter
from FPTree import FPTree
from itertools import combinations
import math
from concurrent import futures

def decimal_round(num):
    t = num * 100000
    t = math.floor(t)
    if t%10 >= 5:
        t+=10
    return "{:.4f}".format(math.floor(t/10)/10000)

class HeaderTable():
    def __init__(self,f_dict=None):
        self.header = dict()
        if f_dict is not None:
            for i in f_dict:
                self.header[i] = {'freq':f_dict[i],'head':None}

    def set_head(self,FP_tree):
        nodes = FP_tree.deep_first(FP_tree.root)
        for node in nodes:
            if node.info is not None:
                if self.header[node.info]['head'] is None:
                    self.header[node.info]['head'] = node
                else:
                    next_node = self.header[node.info]['head']
                    while next_node:
                        t = next_node
                        next_node = next_node.next_node
                    t.next_node = node

    def set_child_head(self,FP_tree,base):
        nodes = FP_tree.deep_first(FP_tree.root)
        for node in nodes:
            if node.info is not None: # not root
                if node.info not in self.header: # no record in header table
                    t = self.header[node.info] ={}
                    t['head'] = node
                    t['freq'] = node.count
                else:
                    next_node = self.header[node.info]['head']
                    while next_node:
                        t = next_node
                        next_node = next_node.next_node
                    t.next_node = node
                    self.header[node.info]['freq'] += node.count

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
    def __init__(self, min_sup,items,OUTPUT_FILE):
        self.i = 1
        self.min_sup = min_sup = float(min_sup)*len(items)
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

        cond_pattern_base = self.build_cond_pattern_base(header_table.header) # { 'a': {'b':4, 'c':2}}

        self.tfp = dict()
        temp_tfp = dict()

        '''
        Frequent Pattern generation
        '''
        '''
        d_len = len(cond_pattern_base)
        th1 = {}
        th2 = {}
        for i,v in enumerate(cond_pattern_base):
            if i<d_len/2:
                th1[v] = cond_pattern_base[v]
            else:
                th2[v] =cond_pattern_base[v]

        with futures.ProcessPoolExecutor() as pool:
            print("submit1")
            pool.submit(self.theadrun,th1)
            print("submit2")
            pool.submit(self.theadrun2,th2)
        '''


        it = iter(self.fpgrowth(cond_pattern_base))
        while True:
            try:
                t = next(it)
                #print(t)
            except StopIteration:
                break


        self.tfp.update(f_dict)

        for i in self.tfp:
            t = sorted(list(map(int,i.split(','))))
            t = list(map(str,t))
            key = ','.join(t)
            temp_tfp[key] = decimal_round(self.tfp[i]/len(items))

        #temp_tfp.update(f_dict)
        temp_tfp = sorted(temp_tfp.items(),key=lambda key: (len(key[0].split(',')),list(map(int,key[0].split(',')))))
        with open(OUTPUT_FILE,'w') as f:
            for i in temp_tfp:
                f.write(str(i[0])+":"+str(i[1])+'\n')

    def theadrun(self,th):
        it = iter(self.fpgrowth(th))
        with open('th1','w') as f:
            while True:
                try:
                    pt = next(it)
                    f.write(pt)
                except StopIteration:
                    break
    def theadrun2(self,th):
        it = iter(self.fpgrowth(th))
        with open('th2','w') as f:
            while True:
                try:
                    pt = next(it)
                    print(pt)
                    f.write(pt)
                except StopIteration:
                    break

    def fpgrowth(self,cond_pattern_base):
        for base in cond_pattern_base:
            FP_tree = FPTree()
            FP_tree.build_child_tree(cond_pattern_base[base],base)  # build child fp tree
            header_table = HeaderTable()
            header_table.set_child_head(FP_tree,base)
            condition_base = self.build_child_base(header_table.header,base)
            if condition_base!={}:
                #print(condition_base)
                #print(self.i,condition_base)
                yield from self.fpgrowth(condition_base)


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

    def build_child_base(self,header,base):
        t = dict()
        for pattern in header:
            next_node = item = header[pattern]['head']
            if header[pattern]['freq'] >= self.min_sup:
                temp_key = pattern+","+base
                self.tfp[temp_key] = header[pattern]['freq']
                #with open('output') as f:
                #yield "123"#(temp_key+':'+str(header[pattern]['freq']))
                #print('==============================',self.i,'==============================')
                #self.i += 1
            while next_node is not None: # header list
                pattern_base = self.get_cpattern_base(next_node,base)
                if pattern_base[0] is not "":
                    try:
                        t[pattern_base[2]][pattern_base[0]] = pattern_base[1]
                    except:
                        t[pattern_base[2]] = {}
                        t[pattern_base[2]][pattern_base[0]] = pattern_base[1]
                next_node = next_node.next_node
        return t

    def get_pattern_base(self,node):
        pattern_len = len(str(node))
        pattern_base = ""
        pattern_count = node.count
        while node.parent is not None:
            pattern_base = str(node)+','+pattern_base
            node = node.parent
        return (pattern_base[:-(pattern_len+2)],pattern_count)

    def get_cpattern_base(self,node,base):
        pattern = str(node)
        pattern_base = ''
        pattern_count = node.count
        while node.parent is not None: # not connect to root which has added to resault
            pattern_base = str(node)+',' + pattern_base
            node = node.parent
        return (pattern_base[:-(len(pattern)+2)],pattern_count,pattern+','+base)


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
