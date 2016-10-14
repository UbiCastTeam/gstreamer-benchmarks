#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

from utils.process import get_stdout

#http://www.raspberrypi-spy.co.uk/2012/09/checking-your-raspberry-pi-board-version/
RPI_REV = {
    '0002': 'Model B',
    '0003': 'Model B',
    '0004': 'Model B',
    '0005': 'Model B',
    '0006': 'Model B',
    '0007': 'Model A',
    '0008': 'Model A',
    '0009': 'Model A',
    '000d': 'Model B',
    '000e': 'Model B',
    '000f': 'Model B',
    '0010': 'Model B+',
    '0011': 'Compute Module',
    '0012': 'Model A+',
    'a01041': 'Pi 2 Model B',
    'a21041': 'Pi 2 Model B',
}

def get_pi_model():
    rev = get_stdout('grep Revision /proc/cpuinfo', shell=True).split(': ')[1].strip()
    return "RaspberryPi %s" %RPI_REV[rev]

def get_machine():
    #x86_64
    #'armv6l'
    #'armv7l'
    return get_stdout('uname -m')

def is_pc():
    machine = get_machine()
    return 'arm' not in machine

def is_intel():
    return 'Intel' in gpu()

def is_pi():
    #BCM2708
    return 'BCM' in get_arm_hw()

def is_jetson():
    return 'jetson' in get_arm_hw()

def get_arm_hw():
    try:
        return get_stdout('grep Hardware /proc/cpuinfo', shell=True).split(': ')[1].strip()
    except Exception:
        return ''

def get_intel_gen():
    try:
        return get_stdout('vainfo | grep "Driver version"', shell=True).split('driver for ')[1].split(' - ')[0]
    except Exception:
        return ''

def gpu():
    if is_pc():
        return get_stdout('lspci | grep -E "VGA|3D"', shell=True).split('controller: ')[1].strip()
    else:
        return get_arm_hw()

def is_nvidia():
    gpu = get_nvidia_gpu()
    return 'NVIDIA' in gpu

def get_nvidia_gpu():
    return get_stdout('lspci | grep VGA', shell=True).strip().split('VGA compatible controller: ')[1]

def cpu_count():
    cpu_count = 1
    with open('/proc/cpuinfo', 'r') as f:
        d = f.read()
        cpu_count = d.count("vendor_id")
    return cpu_count

def cpu():
    if is_pc():
        cpu = get_stdout('cat /proc/cpuinfo | grep "model name" | tail -n 1', shell=True).split(': ')[1].strip()
        if "Intel" in cpu:
            intel_gpu = get_intel_gen()
            if intel_gpu:
                return "%s %s" %(cpu, intel_gpu)
            else:
                nvidia_gpu = get_nvidia_gpu()
                return "%s %s" %(cpu, nvidia_gpu)
    else:
        if is_pi():
            return get_pi_model()
        else:
            return get_arm_hw()
