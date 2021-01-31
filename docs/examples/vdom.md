# VDOM

Let's simulate a VDOM by having the `View.__call__` return a tuple of the string for the greeting and the reference to the resource.
Then, we'll add a method `tree.views.render(view_name)` that does the following:

- Get the view
- Call it
- Concat and return a string

The also means that `Ref` gets a stringable representation to render it.

```{literalinclude} ../../examples/vdom/directives.py
```

And now the "site" code:

```{literalinclude} ../../examples/vdom/__init__.py
```
