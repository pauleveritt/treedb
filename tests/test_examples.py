import pytest

from examples import (
    starting,
    assignment,
    ref,
)


@pytest.mark.parametrize(
    'target',
    [
        starting,
        assignment,
        ref,
    ],
)
def test_examples(target):
    expected, actual = target.run()
    assert actual == expected
