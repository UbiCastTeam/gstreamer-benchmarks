#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016, Florent Thiery

from common.encoding import EncodingTest

def run():
    e = EncodingTest()
    e.COLORSPACE = 'I420'
    e.RAW_BUF_FILE = '/tmp/buf.raw'
    e.RAW_BUF_FILE = '/tmp/buf.raw'
    e.PASS_COUNT = 1
    e.CHANNELS = 1
    e.MAX_BUFFERS = 150
    e.ENABLE_QUALITY_ANALYSIS = True

    e.PLUGINS = [
        ['x264enc', 'x264enc speed-preset=ultrafast bitrate={bitrate_kb} tune=zerolatency key-int-max={keyframes}'],
    ]

    e.PLUGINS_INTEL = [
        ['vaapih264enc', 'vaapih264enc rate-control=2 bitrate={bitrate_kb} keyframe-period={keyframes}'],
        ['vaapih264enc', 'vaapih264enc tune=low-power bitrate={bitrate} keyframe-period={keyframes}'],
    ]

    e.SAMPLES = [
        'pattern=smpte-1920-1080-30',
    ]

    e.BITRATES_K = [
        1000,
        2000,
        5000,
        10000,
        20000,
        40000,
        60000,
        80000,
    ]

    return e.run()
