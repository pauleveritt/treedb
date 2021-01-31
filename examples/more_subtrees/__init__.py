from __future__ import annotations

from dataclasses import dataclass

from .directives import Resource, Tree, View


@dataclass(frozen=True)
class Root(Resource):
    pass


@dataclass(frozen=True)
class RootView(View):

    def __call__(self):
        root = self.ref()
        return f'Hello {root.title}'


def initialize_tree():
    tree = Tree()

    root = Root(name='root', title='My Site')
    tree.resources.set(root)

    root_ref = tree.refs.get('root')
    root_view = RootView(name='root_view', ref=root_ref)
    tree.views.set(root_view)

    return tree


def run():
    tree = initialize_tree()
    root_view = tree.views.get('root_view')
    result1 = root_view()

    new_root = Root(name='root', title='New Site')
    tree.resources.set(new_root)
    result2 = root_view()

    expected = ('Hello My Site', 'Hello New Site')
    actual = (result1, result2)
    return expected, actual
