from pytest import mark


@mark.xfail()
def test_placeholder():
    assert False
