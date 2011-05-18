#!/usr/bin/env python

import os, sys
from os.path import dirname, abspath

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'

parent = dirname(dirname(dirname(abspath(__file__))))
sys.path.insert(0, parent)

from django.test.simple import run_tests


def runtests():
    failures = run_tests(['contrib.BackendsTest'], verbosity=1,
                         interactive=True)
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
