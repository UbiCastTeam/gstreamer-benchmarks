#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

import os
from utils.process import run_cmd
from utils.v4l import v4l_get_current_device

framerates = [60, 30, 25]

resolutions = [
    (3840, 2160),
    (1920, 1200),
    (1920, 1080),
    (1280, 720),
    (1024, 768),
]

cmd_pattern = 'gst-launch-1.0 v4l2src num-buffers=1 device=%s ! "video/x-raw, width=(int)%s, height=(int)%s, framerate=(fraction)%s/1" ! fakesink'

def run():
    results = list()
    at_least_one_success = False
    for f in framerates:
        for r in resolutions:
            info = "Scaling test %sx%s@%s" %(r[0], r[1], f)
            cmd = cmd_pattern %(v4l_get_current_device(), r[0], r[1], f)
            try:
                run_cmd(cmd)
                info = "%s ... success" %info
                print(info)
                at_least_one_success = True
            except Exception as e:
                info = "%s ... failed (pipeline: %s)" %(info, cmd)
                print(info)
            results.append(info)
    return at_least_one_success, "\n\t".join(results) 

if __name__ == '__main__':
    from utils.run import run_test
    run_test(run)
