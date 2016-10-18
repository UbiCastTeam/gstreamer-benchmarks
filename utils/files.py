#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

import os
from utils.process import get_stdout


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
