from __future__ import annotations

from dataclasses import dataclass

from .directives import Resource, Tree, View, Ref, VDOM


@dataclass(frozen=True)
class Root(Resource):
    pass


@dataclass(frozen=True)
class RootView(View):

    def __call__(self) -> VDOM:
        vdom = VDOM(greeting='Hello', ref=self.ref)
        return vdom


def initialize_tree():
    tree = Tree()

    # Now let's change a resource
    new_root = Root(name='root', title='My Site')
    tree.resources.set(new_root)

    root_ref = tree.refs.get('root')
    root_view = RootView(name='root_view', ref=root_ref)
    tree.views.set(root_view)
    return tree


def run():
    # Startup, load the tree
    tree = initialize_tree()

    # A request comes in, render it, which also (now)
    # causes the rendered version to get cached.
    result1 = tree.views.render('root_view')

    # The data changes. This causes a push to all the
    # "subscribers" the use a Ref pointing at this
    # resource. Remember, we're immutable everywhere.
    new_root = Root(name='root', title='New Site')
    tree.update(new_root)

    # A request comes in again. The changed view
    # is already in the cache, so no expensive computation.
    result2 = tree.views.render('root_view')

    expected = ('Hello My Site', 'Hello New Site')
    actual = (result1, result2)
    return expected, actual
