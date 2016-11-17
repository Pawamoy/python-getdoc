#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import inspect
import types


def get_function_doc(function, exclude_function=None):
    if exclude_function:
        for excluded in exclude_function:
            if function.__name__.startswith(excluded):
                return None
    return ('function', function.__name__, inspect.getdoc(function))


def get_class_doc(klass, exclude_class=None, exclude_function=None):
    if exclude_class:
        for excluded in exclude_class:
            if klass.__name__.startswith(excluded):
                return None
    doc = [('class', klass.__name__, inspect.getdoc(klass))]
    class_dict = klass.__dict__
    for item in dir(klass):
        if item in class_dict.keys():
            appended = None
            if isinstance(class_dict[item], type):
                appended = get_class_doc(class_dict[item], exclude_class, exclude_function)
            elif isinstance(class_dict[item], types.FunctionType):
                appended = get_function_doc(class_dict[item], exclude_function)
            if appended is not None:
                doc.append(appended)
    return doc


def get_module_doc(module, exclude_module=None, exclude_class=None, exclude_function=None):
    if exclude_module:
        for excluded in exclude_module:
            if module.__name__.startswith(excluded):
                return None
    doc = [('module', module.__name__, inspect.getdoc(module))]
    code = open(module.__file__).read().encode('utf-8')
    body = ast.parse(code).body
    imported = []
    for node in body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imported.extend([n.name for n in node.names])
    module_dict = module.__dict__
    for item in dir(module):
        if item not in imported and item in module_dict.keys():
            appended = None
            if isinstance(module_dict[item], types.ModuleType):
                appended = get_module_doc(module_dict[item], exclude_module, exclude_class, exclude_function)
            elif isinstance(module_dict[item], type):
                appended = get_class_doc(module_dict[item], exclude_class, exclude_function)
            elif isinstance(module_dict[item], types.FunctionType):
                appended = get_function_doc(module_dict[item], exclude_function)
            if appended is not None:
                doc.append(appended)
    return doc
