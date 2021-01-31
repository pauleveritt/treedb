import pytest

from examples import (
    starting,
    assignment,
    ref,
    tree,
    view_instances,
    ref_instances,
)


@pytest.mark.parametrize(
    'target',
    [
        starting,
        assignment,
        ref,
        tree,
        view_instances,
        ref_instances,
    ],
)
def test_examples(target):
    expected, actual = target.run()
    assert actual == expected
