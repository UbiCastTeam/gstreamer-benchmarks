#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

from utils.process import get_stdout

def get_free_space_bytes(path="/tmp"):
    cmd = "/bin/df %s --output=avail | tail -n 1" %path
    return int(get_stdout(cmd, shell=True))*1024

def get_free_gpu_mem_rpi_bytes():
    cmd = "sudo LD_LIBRARY_PATH=/opt/vc/lib /opt/vc/bin/vcdbg reloc | grep 'free mem' | cut -f 1 | cut -d M -f 1"
    mem_mb = int(get_stdout(cmd, shell=True))*1024*1024
    return 
