# Push VDOM

- Move the logic for clearing the cache, from `update`, to `ViewSubtree`
- Cache the VDOM as well as the string
- Ref objects are smarter, they cache the result of the target
- Have smarter Ref objects in the VDOM

```{literalinclude} ../../examples/push/directives.py
```

And now the "site" code:

```{literalinclude} ../../examples/push/__init__.py
```
