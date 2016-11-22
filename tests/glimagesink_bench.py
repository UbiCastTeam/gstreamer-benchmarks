#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

import os

from utils.time import time_took
from utils.process import run_gst_cmd 
from utils.colors import print_red 

import utils.video as video
import utils.hardware as hw

RAW_BUF_FILE = '/tmp/buf.raw'

cmd_pattern = "gst-launch-1.0 filesrc location=%s blocksize=%%s ! %%s ! glimagesink sync=false" %RAW_BUF_FILE 
#cmd_pattern = "gst-launch-1.0 filesrc location=%s blocksize=%%s ! %%s ! glupload ! fakesink sync=false" %RAW_BUF_FILE 
#cmd_pattern = "gst-launch-1.0 filesrc location=%s blocksize=%%s ! %%s ! glupload ! glvideomixer ! fakesink sync=false" %RAW_BUF_FILE 
#cmd_pattern = "gst-launch-1.0 filesrc location=%s blocksize=%%s ! %%s ! glupload ! glvideomixer ! glimagesink sync=false" %RAW_BUF_FILE 
#cmd_pattern = "gst-launch-1.0 filesrc location=%s blocksize=%%s ! %%s ! glupload ! glcolorconvert ! 'video/x-raw, format=NV12' ! gldownload ! fakesink sync=false" %RAW_BUF_FILE 

RESOLUTIONS = [
    (1920, 1080),
    (3840, 2160),
]

GL_PLATFORMS = [
    'glx',
    'egl',
]

GL_WINDOW = {
    'egl': 'egl',
    'glx': 'x11',
}

# gst_gl_api = 'gles opengl3'

CSP = [
    'I420',
    'NV12',
    'YUY2',
    'UYVY',
    'RGB',
    'RGBA'
]

def get_test_banner():
    info = "glimagesink benchmark, GPU: %s CPU: %s" %(hw.gpu(), hw.cpu())
    info += "\nResolution\tColorspace\tFramerate"
    return info

def run():
    # Ensure that we are not limited by vblank
    os.environ['vblank_mode'] = '0'

    info = get_test_banner()
    for gl_platform in GL_PLATFORMS:
        os.environ['GST_GL_PLATFORM'] = gl_platform
        os.environ['GST_GL_WINDOW'] = GL_WINDOW[gl_platform]
        for colorspace in CSP:
            for resolution in RESOLUTIONS:
                w, h = resolution[0], resolution[1]
                testname = "%sx%s %s" %(w, h, colorspace)
                num_buffers, bufsize, caps = video.generate_buffers_from_pattern(colorspace, w, h, RAW_BUF_FILE)

                cmd = cmd_pattern %(bufsize, caps)

                took = run_gst_cmd(cmd) 
                if took <= 0:
                    print_red('test %s failed' %testname)
                else:
                    # Run it twice to ensure that file was in cache
                    print('Running %s test' %testname)
                    took = run_gst_cmd(cmd)
                    fps = int(round(num_buffers/took))
                    result = "%s\t%sx%s\t%s\t%s" %(gl_platform, w, h, colorspace, fps)
                    print(result)
                    info += "\n%s" %result
    if os.path.exists(RAW_BUF_FILE):
        os.remove(RAW_BUF_FILE)
    return (True, info)

if __name__ == '__main__':
    from utils.run import run_test
    run_test(run)
