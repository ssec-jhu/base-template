import pytest


@pytest.mark.parametrize("value,key", ((1, 1), (2, 2), (3, 3)))
def test_base_dummy(value, key):
    # This test belongs to https://github.com/ssec-jhu/base-template and doesn't actually test anything.
    # Feel free to delete.
    assert value == key
