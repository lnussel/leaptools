#!/usr/bin/python
# Copyright (c) 2016 SUSE LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pprint import pprint
import os, sys, re
import logging
import argparse
import yaml
from xml.etree import cElementTree as ET

logger = logging.getLogger(__name__)

def main(args):

    # do some work here
    logger.info("main")

    with open('lookup.yml', 'r') as fh:
        lookup = yaml.safe_load(fh)

    packages = set()
    develprj = {}
    rings = {}

    with open('sp2', 'r') as fh:
        for line in fh.readlines():
            packages.add(line[:-1])

    for ring in ('ring0', 'ring1', 'ring2'):
        with open(ring, 'r') as fh:
            for line in fh.readlines():
                rings[line[:-1]] = ring

    with open('factory_meta', 'r') as fh:
        root = ET.parse(fh).getroot()
        for p in root.findall('package'):
            name = p.get('name')
            devel = p.find('devel')
            if devel is not None:
                devel = devel.get('project')
            develprj[name] = devel

    grouped = {}

    for p in packages:
        prj = develprj[p] if p in develprj else 'zz_NEW'
        grouped.setdefault(prj, set()).add(p)

    for g in sorted(grouped.keys()):
        print g
        for p in sorted(grouped[g]):
            l = lookup.get(p, '')
            if l.startswith('subpackage '):
                continue
            elif l.startswith('SUSE:SLE-12-SP2:'):
                l = 'SP2'
            elif l.startswith('SUSE:SLE'):
                l = 'SLE'
            elif l.startswith('openSUSE:Leap:42.2:SLE-workarounds'):
                l = 'SLE-hack'
            elif l.startswith('openSUSE:Factory'):
                l = 'Factory'
            elif l.startswith('openSUSE:Leap:42.1'):
                l = '42.1'
            if p in rings:
                print "  %s ## %s @%s" % (p, l, rings[p])
            else:
                print "  %s ## %s" % (p, l)
        print

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='boilerplate python commmand line program')
    parser.add_argument("--dry", action="store_true", help="dry run")
    parser.add_argument("--debug", action="store_true", help="debug output")
    parser.add_argument("--verbose", action="store_true", help="verbose")
    #parser.add_argument("file", nargs='*', help="some file name")

    args = parser.parse_args()

    if args.debug:
        level  = logging.DEBUG
    elif args.verbose:
        level = logging.INFO
    else:
        level = None

    logging.basicConfig(level = level)

    sys.exit(main(args))

# vim: sw=4 et
