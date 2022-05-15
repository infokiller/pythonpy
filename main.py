#!/usr/bin/env python3

# Maybe I can find useful stuff in https://github.com/fish2000/pythonpy-fork

# Imports to be used interactively
import argparse
import collections
import collections.abc
import contextlib
import copy
import csv
import datetime
import decimal
import functools
import glob
import importlib
import inspect
import io
import itertools
import json
import logging
import math
import operator
import os
import pathlib
import pickle
import pprint
import pydoc
import random
import re
import shutil
import subprocess
import sys
import time
import warnings

# pylint: disable=exec-used,eval-used


def run():
    parser = argparse.ArgumentParser(description='pythonpy swiss army knife')
    # group = parser.add_mutually_exclusive_group()
    parser.add_argument('-x',
                        action='store_true',
                        help='Each row of stdin is x')
    parser.add_argument('--pre-cmd',
                        '-c',
                        dest='pre_cmd',
                        help='Run code before expression')
    parser.add_argument('code')
    args = parser.parse_args()
    if not args.code:
        sys.exit('Must provide code argument')
    all_vars_dict = {**globals(), **locals()}
    if not args.x:
        result = eval(args.code, all_vars_dict, locals())
        if result is not None:
            print(result)
        return
    if args.pre_cmd:
        exec(args.pre_cmd, all_vars_dict, locals())
    # pylint: disable-next=possibly-unused-variable,invalid-name
    for line in sys.stdin:
        # x is stdin without the newline
        eval_locals = {**locals(), **{'x': line[:-1]}}
        result = eval(args.code, globals(), eval_locals)
        if result is not None:
            print(result)


def main():
    # https://docs.python.org/3/library/signal.html#note-on-sigpipe
    try:
        run()
    except BrokenPipeError:
        # Python flushes standard streams on exit; redirect remaining output
        # to devnull to avoid another BrokenPipeError at shutdown
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())


if __name__ == '__main__':
    main()
