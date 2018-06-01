# Data Science hw 2

import sys
from FPGrowth import FPGrowth


def input_data(file_name):
    items = []
    with open(file_name,'r') as f:
        for line in f:
            items.append(line[:-1].split(','))
        return items



# INPUT_FILE = 'HW2(sample)/sample.in'

if __name__ == '__main__':
    min_sup = sys.argv[1]
    INPUT_FILE = sys.argv[2]
    OUTPUT_FILE = sys.argv[3]
    items = input_data(INPUT_FILE)
    fp_growth = FPGrowth(min_sup,items,OUTPUT_FILE)
