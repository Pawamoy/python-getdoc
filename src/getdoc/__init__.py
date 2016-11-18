#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
getdoc module.

Provide function to recursively get documentation for a module or a class,
and also for a function. Documentation of objects inside a function definition
will not be retrieved because these objects are created at runtime.

You can filter out modules, classes or functions by defining a new Config object,
or modifying existing ones. Currently, this module provides a default_config and
a django_app_config.
"""

import ast
import inspect
import pkgutil
import re
import types

__version__ = '0.3.0'


class Ex(object):
    """Exclude modules / classes / functions."""

    class Method(object):
        """Enumeration of available methods."""

        PREFIX = 0
        SUFFIX = 1
        CONTAINS = 2
        EXACT = 3
        REGEX = 4

    def __init__(self, value, method=Method.PREFIX):
        self.value = value
        self.method = method

    def match(self, name):
        """Check if passed name matches."""
        if self.method == Ex.Method.PREFIX:
            return name.startswith(self.value)
        elif self.method == Ex.Method.SUFFIX:
            return name.endswith(self.value)
        elif self.method == Ex.Method.CONTAINS:
            return self.value in name
        elif self.method == Ex.Method.EXACT:
            return self.value == name
        elif self.method == Ex.Method.REGEX:
            return re.search(self.value, name)
        return False


class Config(object):
    """Configuration class."""

    def __init__(self,
                 exclude_module=None,
                 exclude_class=None,
                 exclude_function=None,
                 nested_class=False,
                 missing_doc=True):
        self.exclude_module = exclude_module
        self.exclude_class = exclude_class
        self.exclude_function = exclude_function
        self.nested_class = nested_class
        self.missing_doc = missing_doc


default_config = Config(
    exclude_function=[Ex('_')],
    nested_class=False,
    missing_doc=True)

django_app_config = Config(
    exclude_module=[
        Ex('django', Ex.Method.EXACT),
        Ex('django.')],
    exclude_class=[
        Ex('DoesNotExist', Ex.Method.EXACT),
        Ex('MultipleObjectsReturned', Ex.Method.EXACT)],
    exclude_function=[
        Ex('_'),
        Ex('ugettext', Ex.Method.EXACT)],
    nested_class=False,
    missing_doc=True)


def _doc_object(obj, obj_type, nest=None, config=default_config):
    """Return a dict with type, name, doc and nested doc (if any)."""
    doc = inspect.getdoc(obj)

    if not doc and not nest:
        return None

    result = {
        'type': obj_type,
        'name': obj.__name__,
        'doc': doc
    }

    if nest:
        result['nest'] = nest

    return result


def get_function_doc(function, config=default_config):
    """Return doc for a function."""
    if config.exclude_function:
        for ex in config.exclude_function:
            if ex.match(function.__name__):
                return None

    return _doc_object(function, 'function', config=config)


def get_class_doc(klass, config=default_config):
    """Return doc for a class."""
    if config.exclude_class:
        for ex in config.exclude_class:
            if ex.match(klass.__name__):
                return None

    nested_doc = []
    class_dict = klass.__dict__

    for item in dir(klass):
        if item in class_dict.keys():
            appended = None
            if isinstance(class_dict[item], type) and config.nested_class:
                appended = get_class_doc(class_dict[item], config)
            elif isinstance(class_dict[item], types.FunctionType):
                appended = get_function_doc(class_dict[item], config)
            if appended is not None:
                nested_doc.append(appended)

    return _doc_object(klass, 'class', nested_doc, config)


def get_module_doc(module, config=default_config, already_met=None):
    """Return doc for a module."""
    # Avoid recursion loops (init)
    if already_met is None:
        already_met = set()

    if config.exclude_module:
        for ex in config.exclude_module:
            if ex.match(module.__name__):
                return None

    # Force load submodules into module's dict
    if hasattr(module, '__path__'):
        subm = [modname for importer, modname, ispkg in pkgutil.iter_modules(module.__path__)]
        __import__(module.__name__, fromlist=subm)

    # We don't want to include imported items, so we parse the code to blacklist them
    try:
        code = open(module.__file__).read()
        print(code)
        body = ast.parse(code).body
    except SyntaxError:
        code = open(module.__file__).read().encode('utf-8')
        body = ast.parse(code).body
    imported = []
    for node in body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imported.extend([n.name for n in node.names])

    nested_doc = []
    module_dict = module.__dict__

    for item in dir(module):
        if item not in imported and item in module_dict.keys():
            # Avoid recursion loops
            if id(item) in already_met:
                continue
            already_met.add(id(item))

            appended = None
            if isinstance(module_dict[item], types.ModuleType):
                appended = get_module_doc(module_dict[item], config, already_met)
            elif isinstance(module_dict[item], type):
                appended = get_class_doc(module_dict[item], config)
            elif isinstance(module_dict[item], types.FunctionType):
                appended = get_function_doc(module_dict[item], config)
            if appended is not None:
                nested_doc.append(appended)

    return _doc_object(module, 'module', nested_doc, config)
