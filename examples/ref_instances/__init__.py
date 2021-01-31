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
    # The tree now stores resources, views, refs
    items: dict[str, Union[Resource, View, Ref]] = field(default_factory=dict)

    def get(self, name: str) -> Union[Resource, View]:
        return self.items[name]

    def get_ref(self, to: str) -> Ref:
        # Get a ref instance. If it doesn't yet exist, make it
        key = f'ref-{to}'
        if key not in self.items:
            ref = Ref(tree=self, to=to)
            self.items[key] = ref
            return ref
        return self.items[key]

    def set(self, item: Union[Resource, View]):
        self.items[item.name] = item


def initialize_tree():
    tree = Tree()
    root = Root(name='root', title='My Site')
    tree.set(root)

    ref = tree.get_ref('root')
    root_view = RootView(name='root_view', ref=ref)
    tree.set(root_view)

    return tree


@dataclass(frozen=True)
class Ref:
    tree: Tree
    to: str

    def __call__(self):
        r = self.tree.get(self.to)
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
