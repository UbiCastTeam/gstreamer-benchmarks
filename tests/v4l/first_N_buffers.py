#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

import os
from utils.process import get_stdout
from utils.v4l import v4l_get_current_device

cmd_pattern = "gst-launch-1.0 v4l2src device=%s num-buffers=10 ! fakesink silent=false -v | grep chain"

def run():
    failed = False
    for i in range(10):
        success, msg = _run()
        if not success:
            return success, msg
    return success, msg

def _run():
    try:
        data = get_stdout(cmd_pattern %v4l_get_current_device(), shell=True).strip().split('\n')
        last_bufsize = None
        for line in data:
            bufsize = line.split('akesink0:sink) (')[1].split(' bytes, dts')[0]
            if last_bufsize is None:
                last_bufsize = bufsize
            elif bufsize != last_bufsize:
                return (False, "Buffer size varied")
        return (True, "All buffers had the same size")
    except Exception as e:
        print(e)
        return (False, "Error (%s)" %e)

if __name__ == '__main__':
    from utils.run import run_test
    run_test(run)
