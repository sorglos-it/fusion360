# -*- coding: utf-8 -*-
"""Compatibility: the test suite moved to apps/desktop-sketch-grid/tests/test_sketchgrid.py.

This file only forwards, so the old command keeps working:

    python tools/sketch-grid/test_sketchgrid.py

Same output, same exit code.
"""
import os
import sys
import runpy

TARGET = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                      'apps', 'desktop-sketch-grid', 'tests', 'test_sketchgrid.py')

sys.argv[0] = TARGET
runpy.run_path(TARGET, run_name='__main__')
