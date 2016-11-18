=============
python-getdoc
=============

.. start-badges

|travis|
|landscape|
|version|
|wheel|
|gitter|

.. |travis| image:: https://travis-ci.org/Pawamoy/python-getdoc.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/Pawamoy/python-getdoc/

.. |codecov| image:: https://codecov.io/github/Pawamoy/python-getdoc/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/Pawamoy/python-getdoc/

.. |landscape| image:: https://landscape.io/github/Pawamoy/python-getdoc/master/landscape.svg?style=flat
    :target: https://landscape.io/github/Pawamoy/python-getdoc/
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/getdoc.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/getdoc/

.. |wheel| image:: https://img.shields.io/pypi/wheel/getdoc.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/getdoc/

.. |gitter| image:: https://badges.gitter.im/Pawamoy/python-getdoc.svg
    :alt: Join the chat at https://gitter.im/Pawamoy/python-getdoc
    :target: https://gitter.im/Pawamoy/python-getdoc?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


.. end-badges

Simple function to get a python module's doc recursively

License
=======

Software licensed under `MPL 2.0`_ license.

.. _BSD-2 : https://opensource.org/licenses/BSD-2-Clause
.. _MPL 2.0 : https://www.mozilla.org/en-US/MPL/2.0/

Installation
============

::

    pip install getdoc

Documentation
=============

https://github.com/Pawamoy/python-getdoc.wiki

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
