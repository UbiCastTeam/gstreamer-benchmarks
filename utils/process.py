#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery

import os
import subprocess
import shlex

ERRORS = (
    'ERROR',
)

def _run_cmd(cmd, shell=False):
    env = dict(os.environ)
    env["LANG"] = "C"
    if shell:
        args = cmd
    else:
        args = shlex.split(cmd)
    p = subprocess.Popen(args, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=shell)
    stdout, stderr = p.communicate()
    rc = p.returncode
    if rc != 0:
        if '|' in cmd:
            raise Exception('Command %s failed, maybe shell=True is required' %cmd)
        else:
            raise Exception('Command %s failed, error: %s' % (cmd, stderr))
    elif contains_errors(stderr):
        raise Exception('Command %s had an error' %cmd)
    return rc, stdout, stderr

def get_stdout(cmd, shell=False):
    rc, stdout, stderr = _run_cmd(cmd, shell=shell)
    return stdout

def check_cmd(cmd, shell=False, complain=True):
    try:
        _run_cmd(cmd, shell=shell)
        return True, 'no errors'
    except Exception as e:
        if complain:
            print(e)
        return False, e

def run_cmd(cmd, shell=False):
    rc, stdout, stderr = _run_cmd(cmd, shell=shell)

def contains_errors(text):
    for e in ERRORS:
        if e in text:
            return True
