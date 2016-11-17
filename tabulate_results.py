#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

try:
    from tabulate import tabulate
except Exception:
    print('You need to install python-tabulate: sudo pip install tabulate')
    sys.exit()

try:
    fname = sys.argv[1]
    if not os.path.isfile(fname):
        print('File %s not found' % fname)
        sys.exit()
except Exception:
    print('Provide tsv file as argument')
    sys.exit()

try:
    MAX_LEN = int(sys.argv[2])
except Exception:
    MAX_LEN = 30

def limit_size(string, max_len = MAX_LEN):
    if len(string) > max_len:
        return string[:max_len] + '..' 
    return string

with open(fname, 'r') as f:
    d = f.read()
    tabulate_list = []
    for index, line in enumerate(d.split('\n')):
        if index > 0:
            fields = [limit_size(f.strip()) for f in line.split('\t')]
            tabulate_list.append(fields)
        else:
            print('\n' + line + '\n')
    t = tabulate(tabulate_list, headers="firstrow", tablefmt="simple", stralign="center", numalign="center")
    print(t)
    print("\nTable is %s lines wide" % len(t.split('\n')[0]))
