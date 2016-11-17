#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

import os
import time

from statistics import mean

from utils.files import get_timestamped_fname
from utils.process import run_gst_cmd, run_cmd
from utils.colors import print_red 

from utils.gstreamer import is_plugin_present, get_gst_version
import utils.video as video
import utils.hardware as hw

class EncodingTest:

    # ensure that /tmp is a tmpfs or ramfs
    RAW_BUF_FILE = '/tmp/buf.raw'
    RAW_REF_FILE = 'reference.mkv'
    OUTPUT_FOLDER = 'out'
    OUTPUT_FILE_TEMPLATE = 'output-%s.mkv'
    SAMPLES_FOLDER = 'samples'

    PASS_COUNT = 5
    CHANNELS = 3 
    COLORSPACE = 'I420'
    MAX_BUFFERS = 1000

    ENABLE_LIVE = False
    ENABLE_QUALITY_ANALYSIS = False
    QUALITY_METHOD = 'avg_ssim'

    # each plugin is a list: ['plugin_name', 'plugin_bin_description'] 
    # available keys are
    # {bitrate_kb} : bitrate in kbits/s
    # {bitrate} : bitrate in bits/s
    # {keyframes} : GOP (set to 30)
    # {cpu_count} : dynamic, equals to the number of threads on the system
    PLUGINS = [
            ['x264enc', 'x264enc speed-preset=ultrafast bitrate={bitrate_kb} tune=zerolatency key-int-max={keyframes}'],
    ]
    PLUGINS_INTEL = []
    PLUGINS_PI = []
    PLUGINS_JETSON = []
    PLUGINS_NV = []

    BITRATES_K = [
        20000,
    ]

    SAMPLES = [
        'pattern=black-1920-1080-30',
        'pattern=smpte-1920-1080-30',
        'pattern=snow-1920-1080-30',
        'pattern=black-3840-2160-30',
        'pattern=smpte-3840-2160-30',
        'pattern=snow-3840-2160-30',
    ]
    SCAN_SAMPLES = True

    CMD_PATTERN = "gst-launch-1.0 -f filesrc location=%s blocksize=%s ! %s ! tee name=encoder ! %s"

    def write_timestamped_results(self, data):
        fname = get_timestamped_fname()
        with open(fname, 'w') as f:
            f.write(data)
        print('Wrote results to %s' % fname)

    def write_results(self, data, path):
        with open(path, 'w') as f:
            f.write(data)
        print('Wrote %s' % path)

    def get_test_banner(self):
        info = "Gstreamer %s: %s Encoding benchmark (mean fps over %s passes), GPU: %s CPU: %s (live mode: %s)" %(get_gst_version(), self.COLORSPACE, self.PASS_COUNT, hw.gpu(), hw.cpu(), self.ENABLE_LIVE)
        info += "\nEncoder\tSample\tfps\t+/-"
        if self.ENABLE_QUALITY_ANALYSIS:
            info += "\tq\tminq\tqlog"
        return info

    def parse_pattern(self, pattern_string):
        name, w, h, f = pattern_string.split('=')[1].split('-')
        return name, int(w), int(h), int(f)

    def run(self):
        success = False

        if hw.is_intel() and hasattr(self, 'PLUGINS_INTEL'):
            os.environ['LIBVA_DRIVER_NAME'] = 'i965'
            self.PLUGINS.extend(self.PLUGINS_INTEL)
        elif hw.is_nvidia() and hasattr(self, 'PLUGINS_NV'):
            self.PLUGINS.extend(self.PLUGINS_NV)
        else:
            if hw.is_pi() and hasattr(self, 'PLUGINS_PI'):
                self.PLUGINS.extend(self.PLUGINS_PI)
            if hw.is_jetson() and hasattr(self, 'PLUGINS_JETSON'):
                self.PLUGINS.extend(self.PLUGINS_JETSON)

        w = 1920
        h = 1080
        colorspace = self.COLORSPACE
        info = self.get_test_banner()

        available_plugins = list()
        for plugin in self.PLUGINS:
            if is_plugin_present(plugin[0]):
                available_plugins.append(plugin[1])

        if self.SCAN_SAMPLES:
            self.SAMPLES.extend(video.scan_samples_folder(self.SAMPLES_FOLDER))
        total_tests = len(self.SAMPLES) * self.CHANNELS * len(self.PLUGINS) * len(self.BITRATES_K)
        print('About to run %s tests with these samples:\n\t%s' %(total_tests, "\n\t".join(self.SAMPLES)))
        test_count = 0

        for sample in self.SAMPLES:
            num_buffers = None
            if 'pattern' in sample:
                framerate = 30
                sample_name, w, h, framerate = self.parse_pattern(sample)
                num_buffers, bufsize, caps = video.generate_buffers_from_pattern(colorspace, w, h, self.RAW_BUF_FILE, pattern=sample_name, framerate=framerate, max_buffers=self.MAX_BUFFERS)
                input_file = self.RAW_BUF_FILE
            elif 'sample' in sample:
                sample_name, w, h, framerate = video.parse_sample_string(sample)
                input_file_path = os.path.join('samples', sample_name)
                num_buffers, bufsize, caps = video.generate_buffers_from_file(input_file_path, colorspace, w, h, self.RAW_BUF_FILE, framerate=framerate, max_buffers=self.MAX_BUFFERS)
                input_file = self.RAW_BUF_FILE

            output_file_count = 0
            if num_buffers:
                for plugin_string_template in available_plugins:
                    abort = False
                    for channel_count in range(1, self.CHANNELS + 1):
                        output_files = list()
                        for bitrate_kbps in self.BITRATES_K:
                            test_count += 1
                            if not abort:
                                encoding_params = {
                                    'bitrate_kb': bitrate_kbps,
                                    'bitrate': bitrate_kbps*1000,
                                    'keyframes': 30,
                                    'cpu_count': hw.cpu_count(),
                                }
                                plugin_string = plugin_string_template.format(**encoding_params)
                                encoders = list()

                                if self.ENABLE_QUALITY_ANALYSIS:
                                    if not os.path.isdir(self.OUTPUT_FOLDER):
                                        os.mkdir(self.OUTPUT_FOLDER)
                                else:
                                    sink = "fakesink sync=%s" % self.ENABLE_LIVE

                                for i in range(1, channel_count + 1):
                                    if self.ENABLE_QUALITY_ANALYSIS:
                                        output_file_name = self.OUTPUT_FILE_TEMPLATE % output_file_count
                                        sink_pattern = 'matroskamux ! tee name=tee%%s ! queue ! filesink location=%s tee%%s. ! queue ! fakesink sync=%s' % (os.path.join(self.OUTPUT_FOLDER, output_file_name), self.ENABLE_LIVE)
                                        output_files.append(output_file_name)
                                        sink = sink_pattern % (output_file_count, output_file_count)
                                    output_file_count += 1
                                    encoders.append("queue name=enc_%s max-size-buffers=1 ! %s ! %s "  % (i, plugin_string, sink))
                                encoders_string = "encoder. ! ".join(encoders)
                                num_buffers_test = channel_count*num_buffers
                                cmd = self.CMD_PATTERN %(input_file, bufsize, caps, encoders_string)

                                # check cmd and push sample data into RAM
                                print("Heating cache for test %s/%s (%i%%) %s" % (test_count, total_tests, 100*test_count/float(total_tests), plugin_string))
                                took = run_gst_cmd(cmd)
                                if took <= 0:
                                    print_red('<<< Heat test failed: %s' %plugin_string)
                                else:
                                    print('<<< Running test (%s passes, %s channels): %s (%s)' %(self.PASS_COUNT, channel_count, plugin_string, sample))
                                    fps_results = list()
                                    quality_results = list()
                                    min_quality_results = list()
                                    for i in range(self.PASS_COUNT):
                                        # Run it twice to ensure that file was in cache
                                        took = run_gst_cmd(cmd)
                                        if took:
                                            if self.ENABLE_QUALITY_ANALYSIS:
                                                quality, min_quality, quality_log = self.get_quality_score(caps, framerate, output_files)
                                                quality_results.append(quality)
                                                min_quality_results.append(min_quality)
                                            if not self.ENABLE_LIVE:
                                                fps = int(round(num_buffers_test/took))
                                            else:
                                                realtime_duration = num_buffers/framerate
                                                fps = int(round(framerate*(realtime_duration / took)))
                                                # Assuming that encoders should not be late by more than 1 sec 
                                                if int(took) > realtime_duration:
                                                    # If multiple passes are expected, run at least twice
                                                    if self.PASS_COUNT == 1 or (self.PASS_COUNT > 1 and i > 0):
                                                        print('Slower than realtime, aborting next tests')
                                                        abort = True
                                                    else:
                                                        print('Slower than realtime, trying again')
                                        else:
                                            fps = 0
                                        fps_results.append(fps)
                                    sample_desc = "%s-%sch" % (sample, channel_count)
                                    mean_fps = int(round(mean(fps_results)))
                                    variation_fps = int(max(max(fps_results) - mean_fps, mean_fps - min(fps_results)))
                                    result = "%s\t%s\t%s\t%s" %(plugin_string, sample_desc, mean_fps, variation_fps)
                                    if self.ENABLE_QUALITY_ANALYSIS:
                                        result += '\t%.2f\t%.2f\t%s' %(quality, min(min_quality_results), quality_log)
                                    info += "\n%s" %result
                                    success = True
        if os.path.exists(self.RAW_BUF_FILE):
            os.remove(self.RAW_BUF_FILE)
        self.write_timestamped_results(info)
        return (success, info)

    def get_quality_score(self, raw_caps, framerate, files):
        print('Running quality analysis with %s' % self.QUALITY_METHOD)
        muxed_raw_file = os.path.join(self.OUTPUT_FOLDER, self.RAW_REF_FILE)
        cmd = 'gst-launch-1.0 filesrc location=%s ! %s ! matroskamux ! filesink location=%s' % (self.RAW_BUF_FILE, raw_caps, muxed_raw_file)
        rc, stdout, stderr = run_cmd(cmd)
        cmd = 'qpsnr -a %s -o fps=%s -r %s %s' % (self.QUALITY_METHOD, framerate, muxed_raw_file, ' '.join([os.path.join(self.OUTPUT_FOLDER, f) for f in files]))
        rc, stdout, stderr = run_cmd(cmd)
        scores = list()
        header = list()
        warnings = list()
        for index, line in enumerate(stdout.split('\n')):
            if line:
                fields = line.strip(',').split(',')
                if index == 0:
                    header = fields 
                else:
                    frame_count = fields[0]
                    scores_line = [float(f) for f in fields[1:]]
                    for index, score in enumerate(scores_line):
                        scores.append(score)
                        if score < 0.99:
                            warning = 'frame %s of %s is below threshold : %s' % (frame_count, header[index + 1], score)
                            warnings.append(warning)
        os.remove(muxed_raw_file)
        fname = ''
        if warnings:
            fname = os.path.join(self.OUTPUT_FOLDER, '%s-%s.log' % (self.QUALITY_METHOD, int(time.time())))
            self.write_results('\n'.join(warnings), fname)
        return mean(scores), min(scores), fname

if __name__ == '__main__':
    from utils.run import run_test
    t = EncodingTest()
    run_test(t.run)
