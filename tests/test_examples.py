import pytest

from examples import (
    starting,
    assignment,
    ref,
    tree,
    view_instances,
    ref_instances,
    subtrees,
    more_subtrees,
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
        subtrees,
        more_subtrees,
    ],
)
def test_examples(target):
    expected, actual = target.run()
    assert actual == expected
