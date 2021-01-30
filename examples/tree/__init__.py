from dataclasses import dataclass, field


@dataclass(frozen=True)
class Resource:
    name: str  # Used as the key
    title: str


@dataclass(frozen=True)
class Root(Resource):
    pass


@dataclass
class Tree:
    items: dict[str, Resource] = field(default_factory=dict)

    def get(self, name: str) -> Resource:
        return self.items[name]

    def set(self, resource: Resource):
        self.items[resource.name] = resource


def initialize_tree():
    tree = Tree()
    root = Root(name='root', title='My Site')
    tree.set(root)
    return tree


@dataclass(frozen=True)
class Ref:
    tree: Tree
    to: str

    def __call__(self):
        # The *instance* is stored in the view instance.
        # But the actual target isn't looked up until called.
        return self.tree.get(self.to)


@dataclass(frozen=True)
class RootView:
    ref: Ref

    def __call__(self):
        # Resolve the ref then get the attribute
        root = self.ref()
        return f'Hello {root.title}'


def run():
    tree = initialize_tree()

    ref = Ref(tree=tree, to='root')
    root_view = RootView(ref=ref)
    result1 = root_view()

    # Replace the root
    new_root = Root(name='root', title='New Site')
    tree.set(new_root)
    result2 = root_view()

    expected = ('Hello My Site', 'Hello New Site')
    actual = (result1, result2)
    return expected, actual
