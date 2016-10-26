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

    e.PLUGINS = [
            ['x264enc', 'x264enc speed-preset=ultrafast bitrate={bitrate_kb} tune=zerolatency key-int-max={keyframes}'],
    ]

    e.PLUGINS_INTEL = [
            ['vaapih264enc', 'vaapih264enc rate-control=2 bitrate={bitrate_kb} keyframe-period={keyframes}'],
    ]

    e.SAMPLES = [
        'pattern=black-1920-1080-30',
        'sample=test-1920-1080-30.mp4',
    ]
    return e.run()
