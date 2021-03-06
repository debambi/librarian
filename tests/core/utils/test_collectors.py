import pytest

try:
    from unittest import mock
except ImportError:
    import mock

from librarian.core.utils import collectors as mod


MOD = mod.__name__


@pytest.mark.parametrize('val,out', [
    ('', ['']),
    (None, []),
    ('foo', ['foo']),
    (['foo', 'bar'], ['foo', 'bar']),
    (('foo', 'bar'), [('foo', 'bar')]),
])
def test_to_list(val, out):
    assert mod.to_list(val) == out


@pytest.mark.parametrize('obj,name,res', [
    ('foo', 'join', True),
    ('foo', 'bogus', False),
    (1, 'conjugate', True),
    (1, 'numerator', False),  # <-- not callable
])
def test_hasmethod(obj, name, res):
    assert mod.hasmethod(obj, name) == res


def test_doubledot_patterns():
    leading = mod.DOUBLEDOT[0][0]
    assert leading.search('../foo/')
    assert not leading.search('/foo/')
    assert leading.sub('', '../foo/') == 'foo/'

    middle = mod.DOUBLEDOT[1][0]
    assert middle.search('/foo/../bar/')
    assert not middle.search('/foo/..bar/')
    assert middle.sub('/', '/foo/../bar/') == '/foo/bar/'
    assert middle.sub('/', '/foo/../../bar/') == '/foo/bar/'

    trailing = mod.DOUBLEDOT[2][0]
    assert trailing.search('/foo/..')
    assert not trailing.search('/foo/')
    assert trailing.sub('', '/foo/..') == '/foo'


@pytest.mark.parametrize('path,out', [
    ('foo/bar/baz/', 'foo/bar/baz'),
    ('/foo/bar/baz', 'foo/bar/baz'),
    ('foo/bar../baz', 'foo/bar../baz'),
    ('foo/bar..baz/', 'foo/bar..baz'),
    ('../foo/bar', 'foo/bar'),
    ('foo/bar/../../..', 'foo/bar'),
    ('foo/../../../bar', 'foo/bar'),
])
def test_strip_paths(path, out):
    assert mod.strip_path(path) == out


@pytest.mark.parametrize('name,out', [
    ('foo.bar', 'librarian.core.foo.bar'),
    ('.foo.bar', 'librarian.core.foo.bar'),
    ('foo..bar', 'librarian.core.foo.bar'),
    ('foo...bar', 'librarian.core.foo.bar'),
    ('..foo.bar', 'librarian.core.foo.bar'),
    ('foo.bar..', 'librarian.core.foo.bar'),
])
def test_fully_qualified_name(name, out):
    from librarian import core
    assert mod.fully_qualified_name(core, name) == out


def test_muter_basic_iteration():
    m = mod.muter([1, 2, 3])
    out = []
    for i in m:
        out.append(i)
    assert out == [1, 2, 3]


def test_muter_listify():
    m = mod.muter([1, 2, 3])
    assert list(m) == [1, 2, 3]


def test_muter_reset():
    m = mod.muter([1, 2, 3])
    l1 = list(m)
    l2 = list(m)
    m.reset()
    l3 = list(m)
    assert l1 == [1, 2, 3]
    assert l2 == []
    assert l3 == [1, 2, 3]


def test_reset_during_iter():
    m = mod.muter([1, 2, 3])
    v1 = m.next()  # <-- we are at index 1 after this
    m.reset()
    v2 = m.next()  # <-- we are again at index 1 after this
    l = list(m)  # <-- get the remainder
    assert v1 == 1
    assert v2 == 1
    assert l == [2, 3]


def test_append():
    m = mod.muter([1, 2, 3])
    m.append(4)
    assert list(m) == [1, 2, 3, 4]


def test_append_during_iter():
    m = mod.muter([1, 2, 3])
    m.next()  # <-- remaining elements are 2, 3
    m.append(4)
    assert list(m) == [2, 3, 4]


def test_append_during_iter_for_loop():
    append_list = iter([4, 5, 6])

    def appender(obj):
        for i in append_list:
            obj.append(i)
    m = mod.muter([1, 2, 3])
    out = []
    for i in m:
        appender(m)
        out.append(i)
    assert out == [1, 2, 3, 4, 5, 6]


def test_inclusion_test():
    m = mod.muter([1, 2, 3])
    assert 1 in m
    assert 2 in m
    assert 5 not in m


def test_len():
    m = mod.muter([1, 2, 3])
    assert len(m) == 3
    m.append(4)
    assert len(m) == 4
    m.next()
    assert len(m) == 4


def test_remaining():
    m = mod.muter([1, 2, 3])
    out = []
    for i in m:
        out.append(m.remaining)
    assert out == [2, 1, 0]