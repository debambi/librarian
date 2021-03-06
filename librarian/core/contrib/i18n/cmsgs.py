from __future__ import print_function

import fnmatch
import os
import subprocess

from ...exceptions import EarlyExit
from ...exts import ext_container as exts


def convert(po_path):
    base, ext = os.path.splitext(po_path)
    mo_path = base + '.mo'
    subprocess.call(['msgfmt', '-o', mo_path, po_path])


def compile_messages():
    path = os.path.join(exts.config['root'], exts.config['i18n.localedir'])
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, '*.po'):
            if 'LC_MESSAGES' not in root:
                continue
            path = os.path.join(root, f)
            print("Processing '%s'" % path)
            convert(path)
    print('Done')
    raise EarlyExit()
