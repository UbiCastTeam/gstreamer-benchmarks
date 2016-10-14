#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016, Florent Thiery

from common.encoding import EncodingTest

def run():
    e = EncodingTest()
    e.COLORSPACE = 'YUY2'
    e.RAW_BUF_FILE = '/tmp/buf.raw'
    e.PASS_COUNT = 3
    e.PLUGINS = [
        ['x264enc', 'videoconvert ! queue ! x264enc speed-preset=ultrafast bitrate={bitrate_kb} tune=zerolatency key-int-max={keyframes}'],
        ['x265enc', 'videoconvert ! video/x-raw, format=(string)I420 ! queue ! x265enc speed-preset=ultrafast bitrate={bitrate_kb} tune=zerolatency'],
        #['vp8enc', 'videoconvert ! queue ! vp8enc end-usage=cbr target-bitrate={bitrate} keyframe-mode=disabled keyframe-max-dist={keyframes} threads={cpu_count}'],
        #['vp9enc', 'videoconvert ! queue ! vp9enc end-usage=cbr target-bitrate={bitrate} keyframe-mode=disabled keyframe-max-dist={keyframes} threads={cpu_count}'],
        ['jpegenc', 'jpegenc'],
        ['avenc_mjpeg', 'videoconvert ! avenc_mjpeg bitrate={bitrate} gop-size={keyframes}'],
    ]
    e.PLUGINS_INTEL = [
        ['vaapih264enc', 'vaapipostproc ! vaapih264enc rate-control=2 bitrate={bitrate_kb} keyframe-period={keyframes}'],
        ['vaapih265enc', 'vaapipostproc ! vaapih265enc bitrate={bitrate_kb}'],
        ['vaapivp8enc', 'vaapipostproc ! vaapivp8enc bitrate={bitrate_kb} keyframe-period={keyframes}'],
        ['vaapijpegenc', 'vaapipostproc ! vaapijpegenc bitrate={bitrate_kb}'],
        ['vaapih264enc', 'vaapipostproc ! vaapih264enc tune=low-power bitrate={bitrate} keyframe-period={keyframes}'],
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
