from __future__ import annotations

from dataclasses import dataclass, field
# 1. Directive bases
from typing import Sequence, NamedTuple


@dataclass(frozen=True)
class Ref:
    tree: Tree
    to: str

    @property
    def name(self) -> str:
        return self.to

    def __call__(self):
        r = self.tree.resources.get(self.to)
        # We are hardwiring in the returning of a particular attr
        return r.title


@dataclass(frozen=True)
class Resource:
    name: str
    title: str


class VDOM(NamedTuple):
    greeting: str
    ref: Ref


@dataclass(frozen=True)
class View:
    name: str
    ref: Ref

    # Simulate a VDOM with a tuple
    def __call__(self) -> VDOM:
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

    def update(self, resource: Resource):
        """ Given a changed resource, propagate the change """

        # Remember, everything is immutable.

        # 1. Update resource tree
        resource_name = resource.name
        self.resources.set(resource)

        # 2. Find any refs that point to this resource *name*.
        changed_ref_tos = [
            ref.to
            for ref in self.refs.items.values()
            if ref.to == resource_name
        ]

        # 3. Update any views that use those refs
        self.views.update_views(changed_ref_tos)


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


class Rendering(NamedTuple):
    """ Hold the rendering of a view """
    vdom: VDOM
    result: str


@dataclass
class ViewSubtree:
    tree: Tree
    items: dict[str, View] = field(default_factory=dict)
    renderings: dict[str, Rendering] = field(default_factory=dict)

    def get(self, name: str) -> View:
        return self.items[name]

    def render(self, name: str) -> str:
        """ Get and render a view """

        try:
            rendering = self.renderings[name]
            return rendering.result
        except KeyError:
            view = self.items[name]
            vdom = view()
            result = f'{vdom.greeting} {vdom.ref()}'
            rendering = Rendering(vdom=vdom, result=result)
            self.renderings[name] = rendering
            return rendering.result

    def set(self, item: View):
        self.items[item.name] = item

    def update_views(self, changed_refs: Sequence[str]):
        """ Given a list of changed refs, update the views """

        # 3. Find any views that use that ref
        changed_views = [
            view
            for view in self.items.values()
            if view.ref.to in changed_refs
        ]

        for changed_view in changed_views:
            # Later, we'll move this responsibility to the
            # ``ViewSubtree`.
            view_name = changed_view.name
            if view_name in self.renderings:
                # Clear it if in the "cache"
                del self.renderings[view_name]
            self.render(view_name)
