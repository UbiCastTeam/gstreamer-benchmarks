#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

import os
from utils.time import time_took
from utils.process import run_cmd
from utils.v4l import v4l_get_current_device

cmd_pattern = "gst-launch-1.0 v4l2src device=%s num-buffers=1 ! fakesink"

MAX_TIME_S = 1

def _run():
    run_cmd(cmd_pattern %v4l_get_current_device())

def run():
    took = time_took(_run)
    if took < 10:
        took_str = "%ims" %(took*1000)
    else:
        took_str = "%.2fs" %took
    info = "First buffer arrived after %s (max: %ss)" %(took_str, MAX_TIME_S)
    if took <= 0:
        return (False, "Command failed")
    elif took > MAX_TIME_S:
        return (False, info) 
    return (True, info)

if __name__ == '__main__':
    from utils.run import run_test
    run_test(run)
