from dataclasses import dataclass


@dataclass(frozen=True)
class Ref:
    resources: dict[str]
    to: str

    def __call__(self):
        # The *instance* is stored in the view instance.
        # But the actual target isn't looked up until called.
        return self.resources.get(self.to)


@dataclass(frozen=True)
class Root:
    title: str


@dataclass(frozen=True)
class RootView:
    ref: Ref

    def __call__(self):
        # Resolve the ref then get the attribute
        root: Root = self.ref()
        return f'Hello {root.title}'


def run():
    resources = dict(root=Root(title='My Site'))

    # Make a Ref pointing at the collection and contains a path.
    ref = Ref(resources=resources, to='root')
    root_view = RootView(ref=ref)
    result1 = root_view()
    resources['root'] = Root(title='New Site')
    result2 = root_view()

    expected = ('Hello My Site', 'Hello New Site')
    actual = (result1, result2)
    return expected, actual
