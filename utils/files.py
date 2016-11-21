#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

import os
from utils.process import get_stdout
import time
import socket

def read_file(path):
    with open(path, 'r') as f:
        data = f.read()
    return data

def check_temp_path(path='/tmp'):
    path = os.path.dirname(path)
    if not check_path_is_tmpfs(path):
        print('Path %s is not a tmpfs' % path)
        return False
    if not check_path_is_writable(path):
        print('Path %s is not writable' % path)
        return False
    return True

def check_path_is_writable(path='/tmp'):
    return os.access(path, os.W_OK)

def check_path_is_tmpfs(path='/tmp'):
    d = get_stdout('df %s | tail -n 1' % path, shell=True)
    return d.startswith('tmpfs')

def get_timestamped_fname(suffix=None):
    ts = time.strftime('%Y-%m-%d-%H-%M-%S')
    prefix = 'result-%s-%s' % (socket.gethostname().split('.')[0], ts)
    if suffix: 
        prefix += '-%s' % suffix
    fname = prefix + '.txt'
    return fname

def write_timestamped_results(data):
    fname = get_timestamped_fname()
    with open(fname, 'w') as f:
        f.write(data)
    print('Wrote results to %s' % fname)

def write_results(data, path):
    with open(path, 'w') as f:
        f.write(data)
    print('Wrote %s' % path)
