#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

import os
from utils.process import get_stdout
from utils.v4l import v4l_get_current_device

cmd_pattern = "gst-launch-1.0 v4l2src device=%s num-buffers=1 ! fakesink -v | grep v4l2src0"

def run():
    try:
        caps = get_stdout(cmd_pattern %v4l_get_current_device(), shell=True).split('caps = ')[1].strip().replace('\\', '')
        msg = "Default caps are: %s" %caps
        return (True, msg)
    except Exception as e:
        print(e)
        return (False, "Autonegociation failed")

if __name__ == '__main__':
    from utils.run import run_test
    run_test(run)
