#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

def read_file(path):
    with open(path, 'r') as f:
        data = f.read()
    return data
