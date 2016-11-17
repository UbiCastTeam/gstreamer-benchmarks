#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016, Florent Thiery 

import utils.process as process

def is_plugin_present(plugin_name):
    result = process.check_cmd('gst-inspect-1.0 %s &> /dev/null' %plugin_name.split(' ')[0], shell=True, complain=False)[0]
    if not result:
        print('Plugin %s not found' % plugin_name)
    return result

def get_gst_version():
    return process.get_stdout('gst-launch-1.0 --gst-version').strip().split(' ')[-1]
