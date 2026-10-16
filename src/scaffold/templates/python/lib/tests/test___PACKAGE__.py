from __PACKAGE__ import hello


def test_hello():
    assert hello("world") == "hello, world"
