#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

import os
from utils.process import check_cmd 
from utils.v4l import v4l_get_current_device

cmd_pattern = "gst-launch-1.0 v4l2src device=%s num-buffers=1 ! fakesink"  

def run():
    input('Please make sure that input is NOT connected')
    print('Running test')
    result, info = check_cmd(cmd_pattern %v4l_get_current_device())
    input('Please make sure that input connected again')
    return result, info

if __name__ == '__main__':
    from utils.run import run_test
    run_test(run)
