from contextlib import contextmanager
try:
    import coverage
except ImportError:
    coverage = False
import os
from os.path import basename, dirname


from fabric.api import *
from fabric.decorators import task

import os, sys
sys.path.insert(0, os.path.join(os.path.realpath('.'), '..'))

try:
    from d51.django.virtualenv.test_runner import run_tests
except ImportError, e:
    import sys
    sys.stderr.write("This project requires d51.django.virtualenv.test_runner\n")
    sys.exit(-1)

@contextmanager
def html_coverage_report(directory="./coverage"):
    # This relies on this being run from within a directory named the same as
    # the repository on GitHub.  It's fragile, but for our purposes, it works.
    if coverage:
        base_path = os.path.join(dirname(dirname(__file__)), "armstrong")
        files_to_cover = []
        for (dir, dirs, files) in os.walk(base_path):
            if not dir.find("tests") is -1:
                continue
            valid = lambda a: a[0] != "." and a[-3:] == ".py"
            files_to_cover += ["%s/%s" % (dir, file) for file in files if valid(file)]
        cov = coverage.coverage(branch=True, include=files_to_cover)
        cov.start()
    yield

    if coverage:
        cov.stop()
        cov.html_report(directory=directory)
    else:
        print "Install coverage.py to measure test coverage"
