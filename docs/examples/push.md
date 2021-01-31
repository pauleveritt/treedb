# Push

We have been doing a "pull" system.
The view instance never changes.
When a resource changes, the `__call__` "resolves" the reference and gets a new resource instance.

What if we did a "push"?
Whenever the resource changes, it looks through for any references that point to it.
Then, it looks for any views pointing to that matching reference.
When it finds one

Along the way, we teach `ViewSubtree.render` to cache the string results of renderings.
This gives us what we're looking for: views are pre-rendered, and updated on resource change.

```{literalinclude} ../../examples/push/directives.py
```

In the site code you can see the sequence of startup, requests, and state changes.

```{literalinclude} ../../examples/push/__init__.py
```
