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
        # We are hardwiring in the returning of a particular attr
        return r.title


@dataclass(frozen=True)
class Resource:
    name: str
    title: str


@dataclass(frozen=True)
class View:
    name: str
    ref: Ref

    # Simulate a VDOM with a tuple
    def __call__(self) -> tuple[str, Ref]:
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

        # 3. Find any views that use that ref
        changed_views = [
            view
            for view in self.views.items.values()
            if view.ref.to in changed_ref_tos
        ]

        for changed_view in changed_views:
            # Later, we'll move this responsibility to the
            # ``ViewSubtree`.
            view_name = changed_view.name
            if view_name in self.views.renderings:
                # Clear it if in the "cache"
                del self.views.renderings[view_name]
            self.views.render(view_name)


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
    renderings: dict[str, str] = field(default_factory=dict)

    def get(self, name: str) -> View:
        return self.items[name]

    def render(self, name: str) -> str:
        """ Get and render a view """

        try:
            return self.renderings[name]
        except KeyError:
            view = self.items[name]
            greeting, ref = view()
            rendering = f'{greeting} {ref()}'
            self.renderings[name] = rendering
            return rendering

    def set(self, item: View):
        self.items[item.name] = item
