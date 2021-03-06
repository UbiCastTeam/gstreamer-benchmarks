#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016, Florent Thiery

from common.encoding import EncodingTest

def run():
    e = EncodingTest()
    e.COLORSPACE = 'I420'
    e.RAW_BUF_FILE = '/tmp/buf.raw'
    e.PASS_COUNT = 1
    e.CHANNELS = 10
    e.ENABLE_LIVE = True
    e.MAX_BUFFERS = 150
    e.ENABLE_PARALLEL_PLUGINS = True

    e.PLUGINS = [
        ['x264enc', 'x264enc speed-preset=ultrafast bitrate={bitrate_kb} tune=zerolatency key-int-max={keyframes}'],
    ]

    e.PLUGINS_INTEL = [
        ['vaapih264enc tune=none', 'vaapih264enc tune=none rate-control=2 bitrate={bitrate_kb} keyframe-period={keyframes}'],
        ['vaapih264enc tune=low-power', 'vaapih264enc tune=low-power bitrate={bitrate} keyframe-period={keyframes}'],
    ]

    e.SAMPLES = [
        'pattern=black-1920-1080-30',
    ]
    return e.run()
