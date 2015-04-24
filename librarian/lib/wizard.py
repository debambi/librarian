"""
wizard.py: Generic form wizard

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from bottle import request, redirect, mako_template as template

from bottle_utils.common import basestring


class MissingStepHandler(ValueError):

    def __init__(self, index, method):
        msg = 'Missing {0} request handler in step: {1}'.format(method, index)
        super(MissingStepHandler, self).__init__(msg)


class Wizard(object):
    valid_methods = ('GET', 'POST')
    prefix = 'wizard_'
    step_param = 'step'
    start_index = 0
    allow_back = False

    def __init__(self, name):
        self.name = name
        self.steps = dict()

    def __call__(self, *args, **kwargs):
        # each request gets a separate instance so states won't get mixed up
        instance = self.create_wizard(self.name, self.__dict__)
        return instance.dispatch()

    @property
    def __name__(self):
        return self.__class__.__name__

    def dispatch(self):
        # entry-point of a wizard instance, load wizard state from session
        self.load_state()
        self.override_next_step()
        if request.method == 'POST':
            return self.process_current_step()

        return self.start_next_step()

    @property
    def id(self):
        return self.prefix + self.name

    @property
    def step_count(self):
        return len(self.steps)

    @property
    def current_step_index(self):
        return self.state['step']

    def load_state(self):
        state = request.session.get(self.id)
        if not state:
            state = dict(step=self.start_index, data={})
        self.state = state

    def save_state(self):
        request.session[self.id] = self.state

    def next(self):
        """Return next step of the wizard."""
        try:
            step_handlers = self.steps[self.current_step_index]
        except KeyError:
            raise StopIteration()
        else:
            try:
                return step_handlers['GET']
            except KeyError:
                raise MissingStepHandler(self.current_step_index, 'GET')

    def override_next_step(self):
        if self.allow_back:
            override_step = request.params.get(self.step_param)
            if override_step is not None:
                try:
                    step_index = int(override_step)
                except ValueError:
                    return
                else:
                    is_existing_step = step_index in self.steps
                    is_valid_step = step_index <= self.current_step_index
                    if is_existing_step and is_valid_step:
                        self.state['step'] = step_index

    def start_next_step(self):
        try:
            step = next(self)
        except StopIteration:
            return self.wizard_finished(self.state['data'])
        else:
            step_context = step['handler']()
            return template(step['template'],
                            step_index=self.current_step_index,
                            step_count=self.step_count,
                            **step_context)

    def process_current_step(self):
        step_handlers = self.steps[self.current_step_index]
        try:
            step = step_handlers['POST']
        except KeyError:
            raise MissingStepHandler(self.current_step_index, 'POST')

        step_result = step['handler']()
        if not step_result.pop('successful', False):
            return template(step['template'],
                            step_index=self.current_step_index,
                            step_count=self.step_count,
                            **step_result)

        self.state['data'][self.current_step_index] = step_result
        self.state['step'] += 1
        self.save_state()
        if self.allow_back:
            query = '?{0}={1}'.format(self.step_param, self.current_step_index)
            return redirect(request.fullpath + query)

        return self.start_next_step()

    def wizard_finished(self, data):
        raise NotImplementedError()

    def request_step_index(self, name, index, next_free_index):
        if index is None:
            # check if a step is already registered by the same name
            for step_idx, step in self.steps.items():
                if step['name'] == name:
                    return step_idx
            # assign the next available index as no step was registered
            # previously with this name
            return next_free_index
        # index was explicitly specified by registerer, attempt to use it
        try:
            use_index = int(index)
            if use_index < 0:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError('Step index must be a positive integer.')
        else:
            return use_index

    def register_step(self, name, template, method=valid_methods, index=None):
        def decorator(func):
            next_free_index = max(self.steps.keys() + [-1]) + 1
            use_index = self.request_step_index(name, index, next_free_index)

            if (use_index in self.steps and
                    self.steps[use_index]['name'] != name):
                # an auto-indexed handler probably have taken the place of this
                # manually indexed handler, switch their places
                self.steps[next_free_index] = self.steps[use_index]
                del self.steps[use_index]

            methods = [method] if isinstance(method, basestring) else method
            for method_name in methods:
                if method_name not in self.valid_methods:
                    msg = '{0} is not an acceptable HTTP method.'.format(
                        method_name
                    )
                    raise ValueError(msg)
                self.steps.setdefault(use_index, dict(name=name))
                self.steps[use_index][method_name] = {'handler': func,
                                                      'template': template}
            return func
        return decorator

    def remove_gaps(self):
        """Inplace removal of eventual gaps between registered step indexes."""
        original = [None] * (max(self.steps.keys()) + 1)
        for idx, step in self.steps.items():
            original[idx] = step

        gapless = [step for step in original if step is not None]
        self.steps = dict((self.start_index + idx, step)
                          for idx, step in enumerate(gapless))

    @classmethod
    def create_wizard(cls, name, attrs):
        instance = cls(name)
        # make sure attributes that were assigned after the wizard instance was
        # created will be passed on to new instances as well
        for name, value in attrs.items():
            setattr(instance, name, value)

        instance.remove_gaps()
        return instance