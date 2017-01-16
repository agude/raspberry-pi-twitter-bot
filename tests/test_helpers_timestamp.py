import pytest

from rpi_twitter.helpers import timestamp


def test_timestamp():
    result = timestamp()
    sresult = result.split(":")

    # H, M, S = 3
    assert len(sresult) == 3
    for item in sresult:
        assert len(item) == 2
        for char in item:
            assert char.isdigit()
