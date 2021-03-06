#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

import os
from utils.mem import get_free_space_bytes
from utils.files import check_temp_path
from utils.process import run_cmd

COLORSPACES_BPP = {
    'I420': 12,
    'YUY2': 16,
    'UYVY': 16,
    'RGB': 24,
    'RGBA': 32,
    'NV12': 12,
}

TMP_BUF_FILE = 'tmp.raw'

def get_buffer_size_bytes(colorspace, width, height):
    bpp = COLORSPACES_BPP[colorspace]
    return int(round(width*height*bpp/8))

RAW_BUF_FILE = '/tmp/buf.raw'
TEMP_BUF_FILE = 'tmp.raw'

def get_num_buffers_for_path(colorspace, width, height, raw_buf_file, max_buffers=1000):
    bufsize = get_buffer_size_bytes(colorspace, width, height)
    memsize = get_free_space_bytes(os.path.dirname(os.path.abspath(raw_buf_file)))
    return min(int(0.45*memsize/bufsize), max_buffers)

def generate_buffers_from_file(location, colorspace, width, height, raw_buf_file=RAW_BUF_FILE, framerate=30, num_buffers=None, max_buffers=1000):
    if not os.path.exists(location):
        print("Sample %s not found, skipping" % location)
        return None, None, None
    if not check_temp_path(raw_buf_file):
        print("Cannot use temporary file %s, skipping" % raw_buf_file)
        return None, None, None

    print('Generating intermediate raw sample from %s' % location)
    bufsize = get_buffer_size_bytes(colorspace, width, height)
    tmp_location = os.path.join(os.path.dirname(location), TMP_BUF_FILE)
    memsize = get_free_space_bytes(os.path.dirname(os.path.abspath(tmp_location)))
    # assumption: 20 Mbits/s file, build 1s blocks
    #blocksize = int(20*1000*1000/8)
    # FIXME: why is gst-launch-1.0 filesrc location=samples/1080p.mp4 num-buffers=60 blocksize=2500000 ! decodebin ! videoscale ! video/x-raw\,\ format\=\(string\)I420\,\ width\=\(int\)1920\,\ height\=\(int\)1080\,\ framerate\=\(fraction\)30/1 ! filesink location=samples/tmp.raw
    # generating only 53 buffers ?

    # FIXME: try not to convert the whole file
    tmp_num_buffers = 1000
    #tmp_max_size = tmp_num_buffers * blocksize
    #if tmp_max_size > memsize:
    #    print('Not enough space for the whole intermediate raw sample')

    pattern_caps = "video/x-raw\,\ format\=\(string\){colorspace}\,\ width\=\(int\){width}\,\ height\=\(int\){height}\,\ framerate\=\(fraction\){framerate}/1"
    format_dict = {
        'num_buffers': num_buffers,
        'width': width,
        'height': height,
        'colorspace': colorspace,
        'framerate': framerate,
        'raw_buf_file': raw_buf_file,
        'location': location,
        'blocksize': bufsize,
        'tmp_location': tmp_location,
        'tmp_num_buffers': tmp_num_buffers,
    }
    # vaapi decoder sometimes decodes 1080p as 1920x1088 frames, hence the videoscale
    # add videoconvert to fix https://bugzilla.gnome.org/show_bug.cgi?id=772457
    #pattern_gen_buf = "gst-launch-1.0 filesrc location={location} num-buffers={tmp_num_buffers} blocksize={blocksize} ! decodebin ! videoscale ! %s ! filesink location={tmp_location}" % pattern_caps
    pattern_gen_buf = "gst-launch-1.0 filesrc location={location} num-buffers={tmp_num_buffers} ! decodebin ! videoconvert ! videoscale ! %s ! filesink location={tmp_location}" % pattern_caps
    cmd = pattern_gen_buf.format(**format_dict)
    run_cmd(cmd)
    tmp_size = os.path.getsize(tmp_location)

    if not num_buffers:
        num_buffers = format_dict['num_buffers'] = min(get_num_buffers_for_path(colorspace, width, height, raw_buf_file, max_buffers), int(tmp_size/bufsize))
        print('Generate %s buffers (%ss)' % (num_buffers, int(round(num_buffers/framerate))))
    pattern_gen_buf = "gst-launch-1.0 filesrc location={tmp_location} num-buffers={num_buffers} blocksize={blocksize} ! filesink location=%s" % raw_buf_file
    cmd = pattern_gen_buf.format(**format_dict)
    print('Generate final sample')
    run_cmd(cmd)
    #caps = pattern_caps.format(**format_dict) 
    caps = "rawvideoparse width=%s height=%s framerate=%s format=%s" %(width, height, framerate, colorspace.lower())
    if os.path.isfile(tmp_location):
        os.remove(tmp_location)
    return num_buffers, bufsize, caps

def generate_buffers_from_pattern(colorspace, width, height, raw_buf_file=RAW_BUF_FILE, pattern='black', num_buffers=None, framerate=30, max_buffers=1000):
    if not check_temp_path(raw_buf_file):
        print("Cannot use temporary file %s, skipping" % raw_buf_file)
        return None, None, None
    pattern_caps = "video/x-raw\,\ format\=\(string\){colorspace}\,\ width\=\(int\){width}\,\ height\=\(int\){height}\,\ framerate\=\(fraction\){framerate}/1"
    pattern_gen_buf = "gst-launch-1.0 videotestsrc num-buffers={num_buffers} pattern={pattern} ! %s ! filesink location=%s" %(pattern_caps, raw_buf_file)
    if os.path.isfile(raw_buf_file):
        os.remove(raw_buf_file)
    if not num_buffers:
        num_buffers = get_num_buffers_for_path(colorspace, width, height, raw_buf_file, max_buffers)
    format_dict = {
        'num_buffers': num_buffers,
        'duration': int(round(num_buffers/framerate)),
        'pattern': pattern,
        'width': width,
        'height': height,
        'colorspace': colorspace,
        'framerate': framerate,
        'raw_buf_file': raw_buf_file,
    }
    print('Generating {num_buffers} buffers ({duration}s) {width}x{height} {colorspace} with pattern {pattern} to {raw_buf_file}'.format(**format_dict))
    cmd = pattern_gen_buf.format(**format_dict)
    run_cmd(cmd)

    bufsize = get_buffer_size_bytes(colorspace, width, height)
    #caps = pattern_caps.format(**format_dict) 
    caps = "rawvideoparse width=%s height=%s framerate=%s format=%s" %(width, height, framerate, colorspace.lower())
    return num_buffers, bufsize, caps

def scan_samples_folder(folder, extensions=[".mp4", ".qt"]):
    print('Scanning folder %s for samples with these extensions: %s' % (folder, " ".join(extensions)))
    files = list()
    for f in os.listdir(folder):
        sample_string = "sample=%s" % f 
        if os.path.splitext(f)[1] in extensions and check_sample_string(sample_string):
            files.append(sample_string)
    return files

def check_sample_string(sample_string):
    try:
        parse_sample_string(sample_string)
        return True
    except Exception as e:
        print(e)
        print('Sample %s not formatted as expected, should be like bbb-1920-1080-30.mp4' % fname)
        return False

def parse_sample_string(sample_string):
    filename = sample_string.split('=')[1]
    prefix = os.path.splitext(filename)[0]
    w, h, f = prefix.split('-')[1:]
    return filename, int(w), int(h), int(f)
