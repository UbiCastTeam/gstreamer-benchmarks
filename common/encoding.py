#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

import os

from statistics import mean

from utils.time import time_took, get_timestamped_fname
from utils.process import run_cmd
from utils.colors import print_red 

from utils.gstreamer import is_plugin_present, get_gst_version
import utils.video as video
import utils.hardware as hw

class EncodingTest:

    # ensure that /tmp is a tmpfs or ramfs
    RAW_BUF_FILE = '/tmp/buf.raw'
    SAMPLES_FOLDER = 'samples'

    PASS_COUNT = 5
    CHANNELS = 3 
    COLORSPACE = 'I420'

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

    SAMPLES = [
        'pattern=black-1920-1080-30',
        'pattern=smpte-1920-1080-30',
        'pattern=snow-1920-1080-30',
        'pattern=black-3840-2160-30',
        'pattern=smpte-3840-2160-30',
        'pattern=snow-3840-2160-30',
    ]

    CMD_PATTERN = "gst-launch-1.0 -f filesrc location=%s blocksize=%s ! %s ! tee name=encoder ! %s"

    def write_results(self, data):
        fname = get_timestamped_fname()
        with open(fname, 'w') as f:
            f.write(data)
        print('Wrote results to %s' % fname)

    def get_test_banner(self):
        info = "Gstreamer %s: %s Encoding benchmark (%s passes), GPU: %s CPU: %s" %(get_gst_version(), self.COLORSPACE, self.PASS_COUNT, hw.gpu(), hw.cpu())
        info += "\nEncoder\tSample\tMean fps\tMin fps\tMax fps\tMean Mpix/s\tMin Mpix/s\tMax Mpix/s"
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

        bitrate_kbps = 20000
        encoding_params = {
            'bitrate_kb': bitrate_kbps,
            'bitrate': bitrate_kbps*1000,
            'keyframes': 30,
            'cpu_count': hw.cpu_count(),
        }

        self.SAMPLES.extend(video.scan_samples_folder(self.SAMPLES_FOLDER))
        total_tests = len(self.SAMPLES) * self.CHANNELS * len(self.PLUGINS)
        print('About to run %s tests with these samples:\n\t%s' %(total_tests, "\n\t".join(self.SAMPLES)))
        test_count = 0
        for sample in self.SAMPLES:
            num_buffers = None
            if 'pattern' in sample:
                framerate = 30
                sample_name, w, h, framerate = self.parse_pattern(sample)
                num_buffers, bufsize, caps = video.generate_buffers_from_pattern(colorspace, w, h, self.RAW_BUF_FILE, pattern=sample_name, framerate=framerate)
                input_file = self.RAW_BUF_FILE
            elif 'sample' in sample:
                sample_name, w, h, framerate = video.parse_sample_string(sample)
                input_file_path = os.path.join('samples', sample_name)
                num_buffers, bufsize, caps = video.generate_buffers_from_file(input_file_path, colorspace, w, h, self.RAW_BUF_FILE, framerate=framerate)
                input_file = self.RAW_BUF_FILE

            if num_buffers:
                for channel_count in range(1, self.CHANNELS + 1):
                    for plugin_string in available_plugins:
                        plugin_string = plugin_string.format(**encoding_params)
                        encoders = list()
                        for i in range(1, channel_count + 1):
                            encoders.append("queue name=enc_%s max-size-buffers=1 ! %s ! fakesink "  % (i, plugin_string))
                        encoders_string = "encoder. ! ".join(encoders)
                        num_buffers_test = channel_count*num_buffers
                        cmd = self.CMD_PATTERN %(input_file, bufsize, caps, encoders_string)

                        def _run():
                            try:
                                run_cmd(cmd)
                                return True
                            except Exception as e:
                                print(e)
                                return False

                        # check cmd and push sample data into RAM
                        test_count += 1
                        print("Heating cache for test %s/%s (%i%%) %s" % (test_count, total_tests, 100*test_count/float(total_tests), plugin_string))
                        took = time_took(_run)
                        if took <= 0:
                            print_red('<<< Heat test failed: %s' %plugin_string)
                        else:
                            print('<<< Running test (%s passes, %s channels): %s (%s)' %(self.PASS_COUNT, channel_count, plugin_string, sample))
                            fps_results = list()
                            mpx_results = list()
                            for i in range(self.PASS_COUNT):
                                # Run it twice to ensure that file was in cache
                                took = time_took(_run)
                                if took:
                                    fps = int(round(num_buffers_test/took))
                                    mpx = int(round(fps*w*h/1000000))
                                else:
                                    fps = 0
                                    mpx = 0
                                fps_results.append(fps)
                                mpx_results.append(mpx)
                            sample_desc = "%s-%sch" % (sample, channel_count)
                            result = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" %(plugin_string, sample_desc, int(mean(fps_results)), min(fps_results), max(fps_results), int(mean(mpx_results)), min(mpx_results), max(mpx_results))
                            #print(result)
                            info += "\n%s" %result
                            success = True
        if os.path.exists(self.RAW_BUF_FILE):
            os.remove(self.RAW_BUF_FILE)
        self.write_results(info)
        return (success, info)

if __name__ == '__main__':
    from utils.run import run_test
    t = EncodingTest()
    run_test(t.run)
