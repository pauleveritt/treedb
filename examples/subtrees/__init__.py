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
    # Refs are moved out of "items" into an attribute
    items: dict[str, Union[Resource, View]] = field(default_factory=dict)
    refs: RefSubtree = field(init=False)

    def __post_init__(self):
        self.refs = RefSubtree(tree=self)

    def get(self, name: str) -> Union[Resource, View]:
        return self.items[name]

    def set(self, item: Union[Resource, View]):
        self.items[item.name] = item


@dataclass
class RefSubtree:
    tree: Tree
    items: dict[str, Ref] = field(default_factory=dict)

    def get(self, to: str) -> Ref:
        if to not in self.items:
            ref = Ref(tree=self.tree, to=to)
            self.items[to] = ref
            return ref

        return self.items[to]

    def set(self, item: Ref):
        self.items[item.name] = item


def initialize_tree():
    tree = Tree()

    # Initialize the resource subtree
    root = Root(name='root', title='My Site')
    tree.set(root)

    # Make a view and store it, wrongly for now
    root_ref = tree.refs.get('root')
    root_view = RootView(name='root_view', ref=root_ref)
    tree.set(root_view)

    return tree


@dataclass(frozen=True)
class Ref:
    tree: Tree
    to: str

    @property
    def name(self) -> str:
        return self.to

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
