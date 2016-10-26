#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016, Florent Thiery

from common.encoding import EncodingTest

def run():
    e = EncodingTest()
    e.COLORSPACE = 'I420'
    e.RAW_BUF_FILE = '/tmp/buf.raw'
    e.PLUGINS = [
            ['x264enc', 'x264enc speed-preset=ultrafast bitrate={bitrate_kb} tune=zerolatency key-int-max={keyframes}'],
            ['x265enc', 'x265enc speed-preset=ultrafast bitrate={bitrate_kb} tune=zerolatency'],
            #['vp8enc', 'vp8enc end-usage=cbr target-bitrate={bitrate} keyframe-mode=disabled keyframe-max-dist={keyframes} threads={cpu_count}'],
            #['vp9enc', 'vp9enc end-usage=cbr target-bitrate={bitrate} keyframe-mode=disabled keyframe-max-dist={keyframes} threads={cpu_count}'],
            ['jpegenc', 'jpegenc'],
            ['avenc_mjpeg', 'avenc_mjpeg bitrate={bitrate} gop-size={keyframes}'],
    ]

    e.PLUGINS_INTEL = [
            ['vaapih264enc', 'vaapih264enc rate-control=2 bitrate={bitrate_kb} keyframe-period={keyframes}'],
            ['vaapih265enc', 'vaapih265enc bitrate={bitrate_kb}'],
            ['vaapivp8enc', 'vaapivp8enc bitrate={bitrate_kb} keyframe-period={keyframes}'],
            ['vaapijpegenc', 'vaapijpegenc bitrate={bitrate}'],
            ['vaapih264enc', 'vaapih264enc tune=low-power bitrate={bitrate} keyframe-period={keyframes}'],
    ]

    #1.4.4 does not support interval-intraframes prop
    e.PLUGINS_PI = [
        #['omvh264enc', 'omxh264enc control-rate=2 target-bitrate={bitrate} interval-intraframes={keyframes}'],
        ['omxh264enc', 'omxh264enc control-rate=2 target-bitrate={bitrate}'],
    ]

    e.PLUGINS_JETSON = [
        ['omxh264enc', 'omxh264enc control-rate=2 bitrate={bitrate} iframeinterval={keyframes} low-latency=true profile=baseline'],
        ['omxh264enc', 'omxh264enc control-rate=2 bitrate={bitrate} iframeinterval={keyframes} low-latency=true profile=main'],
        ['omxh264enc', 'omxh264enc control-rate=2 bitrate={bitrate} iframeinterval={keyframes} low-latency=true profile=high'],
    ]
    e.SAMPLES = [
        'pattern=black-1920-1080-30',
        'pattern=smpte-1920-1080-30',
        'pattern=snow-1920-1080-30',
        'pattern=black-3840-2160-30',
        'pattern=smpte-3840-2160-30',
        'pattern=snow-3840-2160-30',
        'sample=bbb-1920-1080-30.mp4',
        'sample=bbb-3840-2160-30.mp4',
    ]
    return e.run()
