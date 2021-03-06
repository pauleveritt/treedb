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
    vdom,
    push,
    push_vdom,
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
        vdom,
        push,
        push_vdom,
    ],
)
def test_examples(target):
    expected, actual = target.run()
    assert actual == expected
