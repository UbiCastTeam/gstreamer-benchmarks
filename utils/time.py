#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

import time
import socket

def time_took(function):
    before = time.time()
    try:
        success = function()
    except Exception as e:
        print('Error: %s' %e)
        return 0
    after = time.time()
    took = (after - before) if success else 0
    return took

def time_took_ms(function):
    return time_took(function)*1000

def get_timestamped_fname():
    ts = int(time.time())
    return "result-%s-%s.txt" % (socket.gethostname(), ts)
