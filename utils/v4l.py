#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

import os

def v4l_get_name(device='video0'):
    path_pattern = "/sys/class/video4linux/%s/name"
    from utils.files import read_file
    path = path_pattern %device
    return read_file(path).strip() 

def v4l_get_devices():
    return os.listdir('/sys/class/video4linux')

def v4l_set_current_device(device):
    os.environ['V4L2_TEST_DEVICE'] = device

def v4l_get_current_device():
    return os.environ.get('V4L2_TEST_DEVICE', '/dev/video0')
