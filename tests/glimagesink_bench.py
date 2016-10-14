#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

import os

from utils.time import time_took
from utils.process import run_cmd
from utils.colors import print_red 

import utils.video as video
import utils.hardware as hw

RAW_BUF_FILE = '/tmp/buf.raw'

cmd_pattern = "gst-launch-1.0 filesrc location=%s blocksize=%%s ! %%s ! glimagesink sync=false" %RAW_BUF_FILE 

def get_test_banner():
    info = "glimagesink benchmark, GPU: %s CPU: %s" %(hw.gpu(), hw.cpu())
    info += "\nResolution\tColorspace\tFramerate"
    return info

def run():
    # Ensure that we are not limited by vblank
    os.environ['vblank_mode'] = '0'

    info = get_test_banner()
    for colorspace in video.COLORSPACES_BPP:
        for resolution in video.RESOLUTIONS:
            w, h = resolution[0], resolution[1]
            testname = "%sx%s %s" %(w, h, colorspace)
            num_buffers, bufsize, caps = video.generate_buffers(colorspace, w, h, RAW_BUF_FILE)

            cmd = cmd_pattern %(bufsize, caps)
            def _run():
                run_cmd(cmd)

            took = time_took(_run)
            if took <= 0:
                print_red('test %s failed' %testname)
            else:
                # Run it twice to ensure that file was in cache
                print('Running %s test' %testname)
                took = time_took(_run)
                fps = int(round(num_buffers/took))
                result = "%sx%s\t%s\t%s" %(w, h, colorspace, fps)
                print(result)
                info += "\n%s" %result
    if os.path.exists(RAW_BUF_FILE):
        os.remove(RAW_BUF_FILE)
    return (True, info)

if __name__ == '__main__':
    from utils.run import run_test
    run_test(run)
