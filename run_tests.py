#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

import os
import sys
import imp

from utils.v4l import v4l_get_name, v4l_get_devices, v4l_set_current_device
from utils.colors import Colors

TESTS_DIR = 'tests'

def scan_test_folder(folder=TESTS_DIR):
    test_files = list()
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith('.py'):
                test_files.append(os.path.join(root, f))
    return test_files

def run_tests(test_files):
    print('Will run the following tests \n\t%s' % "\n\t".join(test_files))
    results = list()

    for test_file in test_files:
        test_name = os.path.splitext(test_file)[0]
        test_module = imp.load_source(test_name, test_file)

        if hasattr(test_module, 'get_test_banner'):
            banner = test_module.get_test_banner()
        else:
            banner = "Test: %s" %(test_name)

        def run_test(test_module, test_banner):
            print("\n>>> Running %s" %test_banner)
            #results.append("\n%s" %test_banner)
            result, t_info = test_module.run()
            if result:
                info = "%s[Pass]%s" %(Colors.GREEN, Colors.DEFAULT)
            else:
                info = "%s[Fail]%s" %(Colors.RED, Colors.DEFAULT)
            info = "%s\n%s\n" %(info, t_info)
            print("Result:%s\n<<<Finished" %info)
            return info

        if "v4l" in test_name:
            test_name = os.path.basename(test_name)
            for device in v4l_get_devices():
                device_path = '/dev/%s' %device
                banner = 'V4L %s test of device %s (%s)' %(test_name, v4l_get_name(), device_path)
                v4l_set_current_device(device_path)
                results.append(run_test(test_module, banner))
            else:
                print('No V4L device found, skipping test %s' %test_name)
        else:
            results.append(run_test(test_module, banner))
    print('\n###########################################')
    print('####### Tests finished, results ###########')
    print('###########################################\n')
    print("\n".join(results))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test-list", help="csv-separated list of tests to run, defaults to All")
    parser.add_argument("-l", "--list-tests", help="list all available tests", action="store_true")
    args = parser.parse_args()
    if args.list_tests:
        print('Available tests:\n\t%s' %'\n\t'.join(scan_test_folder()))
        sys.exit()
    if args.test_list:
        test_files_arg = args.test_list.split(',')
        test_files = list()
        for f in test_files_arg:
            if os.path.isdir(f):
                test_files.extend(scan_test_folder(f))
            else:
                test_files.append(f)
        run_tests(test_files)
    else:
        run_tests(scan_test_folder())
