# Subtrees

We have some leaks.
Let's re-organize our tree to have a subtree for instances of each "kind of thing", starting with `RefSubtree`.
These subtree containers are then managers for their "kinds of things".

```{literalinclude} ../../examples/subtrees/__init__.py
```
