from dataclasses import dataclass


@dataclass
class Root:
    title: str


@dataclass
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

    # Change the title of root, get another view result
    resources['root'].title = 'New Site'
    result2 = root_view()

    expected = ('Hello My Site', 'Hello New Site')
    actual = (result1, result2)
    return expected, actual
