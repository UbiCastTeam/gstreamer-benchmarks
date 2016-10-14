#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

def run_test(run_function):
    result, info = run_function()
    if result:
        print('[Pass] %s' %info)
    else:
        print('[Fail] %s' %info)
    return result, info
