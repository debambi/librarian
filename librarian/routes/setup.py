"""
setup.py: Basic setup wizard steps

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import os

from streamline import NonIterableRouteBase, TemplateRoute

from ..core.contrib.templates.renderer import template
from ..core.exts import ext_container as exts
from ..helpers.ondd import has_tuner
from ..utils.route_mixins import RedirectRouteMixin


def iter_lines(lines):
    while lines:
        yield lines.pop()


def iter_log(file_obj, last_n_lines):
    return iter_lines(list(file_obj)[-last_n_lines:])


class Diag(TemplateRoute):
    path = '/diag/'
    template_func = template
    template_name = 'diag'
    exclude_plugins = ['setup_plugin']

    #: Default number of lines to be returned from the tail of a logfile
    DEFAULT_LINES = 100

    def get_lines(self):
        try:
            return int(self.request.params.get('lines', self.DEFAULT_LINES))
        except (ValueError, TypeError):
            return self.DEFAULT_LINES

    def get_log_iterator(self):
        logpath = self.config['logging.syslog']
        if not os.path.exists(logpath):
            return []

        lines = self.get_lines()
        with open(logpath, 'rt') as log:
            return iter_log(log, lines)

    def get(self):
        if exts.setup_wizard.is_completed:
            return self.redirect('/')
        return dict(logs=self.get_log_iterator(),
                    has_tuner=has_tuner())


class Enter(NonIterableRouteBase):
    path = '/setup/'
    exclude_plugins = ['setup_plugin']

    def get(self):
        return exts.setup_wizard()

    def post(self):
        return exts.setup_wizard()


class Exit(RedirectRouteMixin, NonIterableRouteBase):
    path = '/setup/exit/'
    exclude_plugins = ['setup_plugin']

    def get(self):
        exts.setup_wizard.exit()
        self.perform_redirect()
