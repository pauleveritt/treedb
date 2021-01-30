from dataclasses import dataclass


# Just to emphasize, we make these "immutable"
@dataclass(frozen=True)
class Root:
    title: str

# Just to emphasize, we make these "immutable"
@dataclass(frozen=True)
class RootView:
    root: Root

    def __call__(self):
        return f'Hello {self.root.title}'


def run():
    # Make a "database" of resources
    resources = dict(root=Root(title='My Site'))

    # Generate a view *instance*
    root_view = RootView(root=resources['root'])

    # Use the view to get a result
    result1 = root_view()

    # Change *instance* instead of the attribute
    resources['root'] = Root(title='New Site')
    # root_view still points to the previous Root instance
    result2 = root_view()

    # Uh oh, it didn't change
    expected = ('Hello My Site', 'Hello My Site')
    actual = (result1, result2)
    return expected, actual
