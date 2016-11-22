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

#MAX_BUFFERS = 90
MAX_BUFFERS = 1000

GST_GL_PLATFORMS = [
    'glx',
    'egl',
]

GST_GL_WINDOW = {
    #'egl': ['wayland', 'x11', 'dispmanx', 'android'],
    'egl': ['x11'],
    'glx': ['x11'],
}
# glx: x11 only
# GST_GL_WINDOW=x11 under wayland will use xwayland 
# egl: wayland x11, android, dispmanx (pi/broadcom)
# window: "whatever" creates dummy window
# only the pi supports opengl without xorg/wayland 

GST_GL_API = ['gles2', 'opengl', 'opengl3']

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
    info += "\nTest\tFramerate"
    return info

def run():
    # Ensure that we are not limited by vblank
    os.environ['vblank_mode'] = '0'

    info = get_test_banner()
    for gl_platform in GST_GL_PLATFORMS:
        os.environ['GST_GL_PLATFORM'] = gl_platform
        gl_windows = GST_GL_WINDOW[gl_platform]
        for gl_window in gl_windows:
            os.environ['GST_GL_WINDOW'] = gl_window 
            for gl_api in GST_GL_API:
                os.environ['GST_GL_API'] = gl_api
                for colorspace in CSP:
                    for resolution in RESOLUTIONS:
                        w, h = resolution[0], resolution[1]
                        testname = "%s %s %s %sx%s %s" %(gl_platform, gl_window, gl_api, w, h, colorspace)
                        num_buffers, bufsize, caps = video.generate_buffers_from_pattern(colorspace, w, h, RAW_BUF_FILE, max_buffers=MAX_BUFFERS)

                        cmd = cmd_pattern %(bufsize, caps)

                        took = run_gst_cmd(cmd) 
                        if took <= 0:
                            print_red('test %s failed' %testname)
                        else:
                            # Run it twice to ensure that file was in cache
                            print('Running %s test' %testname)
                            took = run_gst_cmd(cmd)
                            fps = int(round(num_buffers/took))
                            result = "%s\t%s" %(testname, fps)
                            print(result)
                            info += "\n%s" %result
    if os.path.exists(RAW_BUF_FILE):
        os.remove(RAW_BUF_FILE)
    return (True, info)

if __name__ == '__main__':
    from utils.run import run_test
    run_test(run)
