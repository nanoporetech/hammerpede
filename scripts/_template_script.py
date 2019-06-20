#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Template script.
"""

import argparse
import sys

"""
Parse command line arguments.
"""
parser = argparse.ArgumentParser(
    description='Template script.')
parser.add_argument(
    '-i', metavar='input', type=str, help="Input.")


if __name__ == '__main__':
    args = parser.parse_args()
