from __future__ import annotations

from dataclasses import dataclass, field


# 1. Directive bases
@dataclass(frozen=True)
class Ref:
    tree: Tree
    to: str

    @property
    def name(self) -> str:
        return self.to

    def __call__(self):
        r = self.tree.resources.get(self.to)
        return self.tree.resources.get(self.to)


@dataclass(frozen=True)
class Resource:
    name: str
    title: str


@dataclass(frozen=True)
class View:
    name: str
    ref: Ref

    def __call__(self) -> str:
        ...


# 2. Subtrees that manage their instances

@dataclass
class Tree:
    refs: RefSubtree = field(init=False)
    resources: ResourceSubtree = field(init=False)
    views: ViewSubtree = field(init=False)

    def __post_init__(self):
        self.refs = RefSubtree(tree=self)
        self.resources = ResourceSubtree(tree=self)
        self.views = ViewSubtree(tree=self)


@dataclass
class RefSubtree:
    tree: Tree
    items: dict[str, Ref] = field(default_factory=dict)

    def get(self, name: str) -> Ref:
        if name not in self.items:
            ref = Ref(tree=self.tree, to=name)
            self.items[name] = ref
            return ref

        return self.items[name]

    def set(self, item: Ref):
        self.items[item.name] = item


@dataclass
class ResourceSubtree:
    tree: Tree
    items: dict[str, Resource] = field(default_factory=dict)

    def get(self, name: str) -> Resource:
        return self.items[name]

    def set(self, item: Resource):
        self.items[item.name] = item


@dataclass
class ViewSubtree:
    tree: Tree
    items: dict[str, View] = field(default_factory=dict)

    def get(self, name: str) -> View:
        return self.items[name]

    def set(self, item: View):
        self.items[item.name] = item
