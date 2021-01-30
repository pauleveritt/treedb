import pytest

from examples import (
    starting,
    assignment,
)


@pytest.mark.parametrize(
    'target',
    [
        starting,
        assignment,
    ],
)
def test_examples(target):
    expected, actual = target.run()
    assert expected == actual
