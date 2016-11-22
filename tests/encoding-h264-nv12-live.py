#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016, Florent Thiery

from common.encoding import EncodingTest

def run():
    e = EncodingTest()
    e.COLORSPACE = 'NV12'
    e.RAW_BUF_FILE = '/tmp/buf.raw'
    e.ENABLE_LIVE = True
    e.CHANNELS = 20
    e.PLUGINS = [
            ['x264enc', 'x264enc speed-preset=ultrafast bitrate={bitrate_kb} tune=zerolatency key-int-max={keyframes}'],
    ]
    e.PLUGINS_INTEL = [
            ['vaapih264enc tune=none', 'vaapih264enc tune=none rate-control=2 bitrate={bitrate_kb} keyframe-period={keyframes}'],
            ['vaapih264enc tune=low-power', 'vaapih264enc tune=low-power bitrate={bitrate} keyframe-period={keyframes}'],
    ]
    e.PLUGINS_JETSON = [
        ['omxh264enc', 'omxh264enc control-rate=2 bitrate={bitrate} iframeinterval={keyframes} low-latency=true profile=baseline'],
        ['omxh264enc', 'omxh264enc control-rate=2 bitrate={bitrate} iframeinterval={keyframes} low-latency=true profile=main'],
        ['omxh264enc', 'omxh264enc control-rate=2 bitrate={bitrate} iframeinterval={keyframes} low-latency=true profile=high'],
    ]
    e.PLUGINS_NV = [
        ['nvh264enc', 'nvh264enc preset=default bitrate={bitrate_kb} rc-mode=2'],
        ['nvh264enc', 'nvh264enc preset=hp bitrate={bitrate_kb} rc-mode=2'],
        ['nvh264enc', 'nvh264enc preset=hq bitrate={bitrate_kb} rc-mode=2'],
        ['nvh264enc', 'nvh264enc preset=low-latency bitrate={bitrate_kb} rc-mode=2'],
        ['nvh264enc', 'nvh264enc preset=low-latency-hq bitrate={bitrate_kb} rc-mode=2'],
        ['nvh264enc', 'nvh264enc preset=low-latency-hp bitrate={bitrate_kb} rc-mode=2'],
    ]
 
    e.SAMPLES = [
        'pattern=black-1920-1080-30',
        'pattern=smpte-1920-1080-30',
        'pattern=snow-1920-1080-30',
        'pattern=black-3840-2160-30',
        'pattern=smpte-3840-2160-30',
        'pattern=snow-3840-2160-30',
    ]
    return e.run()
