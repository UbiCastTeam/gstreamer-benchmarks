#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016, Florent Thiery

from common.encoding import EncodingTest

def run():
    e = EncodingTest()
    e.COLORSPACE = 'I420'
    e.RAW_BUF_FILE = '/tmp/buf.raw'
    e.PASS_COUNT = 1
    e.CHANNELS = 1
    e.ENABLE_QUALITY_ANALYSIS =  True

    e.PLUGINS = [
        ['x264enc', 'x264enc speed-preset=ultrafast bitrate={bitrate_kb} tune=zerolatency key-int-max={keyframes}'],
        ['x264enc', 'x264enc speed-preset=superfast bitrate={bitrate_kb} tune=zerolatency key-int-max={keyframes}'],
        ['x264enc', 'x264enc speed-preset=veryfast bitrate={bitrate_kb} tune=zerolatency key-int-max={keyframes}'],
        ['x264enc', 'x264enc speed-preset=faster bitrate={bitrate_kb} tune=zerolatency key-int-max={keyframes}'],
        ['x264enc', 'x264enc speed-preset=fast bitrate={bitrate_kb} tune=zerolatency key-int-max={keyframes}'],
        ['x264enc', 'x264enc speed-preset=medium bitrate={bitrate_kb} tune=zerolatency key-int-max={keyframes}'],
        ['x264enc', 'x264enc speed-preset=slow bitrate={bitrate_kb} tune=zerolatency key-int-max={keyframes}'],
        ['x264enc', 'x264enc speed-preset=slower bitrate={bitrate_kb} tune=zerolatency key-int-max={keyframes}'],
        ['x264enc', 'x264enc speed-preset=veryslow bitrate={bitrate_kb} tune=zerolatency key-int-max={keyframes}'],
    ]

    e.PLUGINS_INTEL = [
        ['vaapih264enc', 'vaapih264enc rate-control=2 bitrate={bitrate_kb} keyframe-period={keyframes}'],
        ['vaapih264enc', 'vaapih264enc tune=low-power bitrate={bitrate} keyframe-period={keyframes}'],
    ]

    e.SAMPLES = [
        'pattern=black-1920-1080-30',
        'pattern=smpte-1920-1080-30',
        'pattern=snow-1920-1080-30',
    ]
    return e.run()
