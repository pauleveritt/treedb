# Push

We have been doing a "pull" system.
The view instance never changes.
When a resource changes, the `__call__` "resolves" the reference and gets a new resource instance.

What if we did a "push"?
Whenever the resource changes, it looks through for any references that point to it.
Then, it looks for any views pointing to that matching reference.
When it finds one

```{literalinclude} ../../examples/push/directives.py
```

And now the "site" code:

```{literalinclude} ../../examples/push/__init__.py
```
