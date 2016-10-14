#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016, Florent Thiery 

class Colors():
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    TEAL = '\033[96m'
    DEFAULT = '\033[0m'

def print_red(text):
    print("%s%s%s" %(Colors.RED, text, Colors.DEFAULT))

def print_green(text):
    print("%s%s%s" %(Colors.GREEN, text, Colors.DEFAULT))
