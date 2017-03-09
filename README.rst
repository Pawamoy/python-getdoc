=============
Python getdoc
=============

.. start-badges


|travis|
|version|
|wheel|
|pyup|
|gitter|


.. |travis| image:: https://travis-ci.org/Pawamoy/python-getdoc.svg?branch=master
    :target: https://travis-ci.org/Pawamoy/python-getdoc/
    :alt: Travis-CI Build Status

.. |pyup| image:: https://pyup.io/repos/github/Pawamoy/python-getdoc/shield.svg
    :target: https://pyup.io/repos/github/Pawamoy/python-getdoc/
    :alt: Updates

.. |gitter| image:: https://badges.gitter.im/Pawamoy/python-getdoc.svg
    :target: https://gitter.im/Pawamoy/python-getdoc
    :alt: Join the chat at https://gitter.im/Pawamoy/python-getdoc

.. |version| image:: https://img.shields.io/pypi/v/getdoc.svg?style=flat
    :target: https://pypi.python.org/pypi/getdoc/
    :alt: PyPI Package latest release

.. |wheel| image:: https://img.shields.io/pypi/wheel/getdoc.svg?style=flat
    :target: https://pypi.python.org/pypi/getdoc/
    :alt: PyPI Wheel


.. end-badges

Simple function to get a python module's doc recursively.

License
=======

Software licensed under `ISC`_ license.

.. _ISC: https://www.isc.org/downloads/software-support-policy/isc-license/

Installation
============

::

    pip install getdoc

Documentation
=============

http://python-getdoc.readthedocs.io/en/latest/


Development
===========

To run all the tests: ``tox``

Usage
=====

.. code:: python

    import some_module
    from getdoc import get_module_doc

    doc = get_module_doc(some_module)
    # The result is a dictionnary: {type, name, doc, [nested_doc]},
    # type being 'function', 'class', or 'module',
    # and nested_doc being a list of dictionnaries as above.

You can get doc for just a class (and its contents), or just a function.

.. code:: python

    from getdoc import get_class_doc, get_function_doc

    doc = get_class_doc(some_module.SomeClass)
    doc = get_function_doc(some_module.SomeClass.some_function)

A bit more advanced...

.. code:: python

    # You can exclude modules, classes or functions with a Config instance.
    from getdoc import Config, Ex, default_config, django_app_config

    # The following is equal to django_app_config
    custom_config = Config(
        exclude_module=[
            Ex('django', Ex.Method.EXACT),
            Ex('django.')],
        exclude_class=[
            Ex('DoesNotExist', Ex.Method.EXACT),
            Ex('MultipleObjectsReturned', Ex.Method.EXACT)],
        exclude_function=[
            Ex('_'),
            Ex('ugettext', Ex.Method.EXACT)],
        nested_class=False,  # Don't get doc for nested class
        missing_doc=True)  # Still return items if no doc and no nested doc

    doc = get_module_doc(some_module, config=custom_config)

Default method for exclusion is PREFIX.
There is also SUFFIX, EXACT, CONTAINS, REGEX.
