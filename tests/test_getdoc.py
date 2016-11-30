import getdoc
from getdoc import Config, Ex, get_class_doc, get_function_doc, get_module_doc


def test_main():
    assert getdoc


def test_module_doc():
    module_doc = get_module_doc(getdoc)
    assert module_doc


def test_class_doc():
    class_doc = get_class_doc(Config)
    assert class_doc


def test_class_doc_nested():
    from getdoc import default_config
    default_config.nested_class = True
    class_doc_nested = get_class_doc(Ex, config=default_config)
    assert class_doc_nested
    assert 'Method' in [d['name'] for d in class_doc_nested['nest']]


def test_function_doc():
    function_doc = get_function_doc(get_module_doc)
    assert function_doc
