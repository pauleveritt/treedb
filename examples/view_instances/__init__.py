from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union


@dataclass(frozen=True)
class Resource:
    name: str
    title: str


@dataclass(frozen=True)
class Root(Resource):
    pass


@dataclass
class Tree:
    # The tree now stores resources and views
    items: dict[str, Union[Resource, View]] = field(default_factory=dict)

    def get(self, name: str) -> Union[Resource, View]:
        return self.items[name]

    def set(self, item: Union[Resource, View]):
        self.items[item.name] = item


def initialize_tree():
    tree = Tree()
    root = Root(name='root', title='My Site')
    tree.set(root)

    # Also add a view instance that has a ref. It's a freaky
    # idea...views can be partially
    ref = Ref(tree=tree, to='root')
    root_view = RootView(name='root_view', ref=ref)
    tree.set(root_view)

    return tree


@dataclass(frozen=True)
class Ref:
    tree: Tree
    to: str

    def __call__(self):
        return self.tree.get(self.to)


@dataclass(frozen=True)
class View:
    name: str
    ref: Ref

    def __call__(self) -> str:
        ...


@dataclass(frozen=True)
class RootView(View):

    def __call__(self):
        root = self.ref()
        return f'Hello {root.title}'


def run():
    tree = initialize_tree()
    root_view = tree.get('root_view')
    result1 = root_view()

    new_root = Root(name='root', title='New Site')
    tree.set(new_root)
    result2 = root_view()

    expected = ('Hello My Site', 'Hello New Site')
    actual = (result1, result2)
    return expected, actual
