# More Subtrees

Let's finish the subtree work by making subtrees for `ResourceSubtree` and `ViewSubtree`.
These subtrees -- duh -- store instances (and later, a tree of instances) of their kinds of things.

These 3 concepts -- `Resource`, `View`, and `Ref` have some similarities:

- They are the main entities in our system
- Each are actually base classes, or interfaces, or protocols, or something
- But they are starting to play a role as specialized factories
- And, their subclass instances have a place in the tree
- That place in the tree also has some policies for dealing with instances

Let's make a concept called "directive" for those kinds of things, then put them in a file called `directives.py`:

```{literalinclude} ../../examples/more_subtrees/directives.py
```

Here then is the code that uses that system with custom classes -- i.e. a "site" -- to generate a result.

```{literalinclude} ../../examples/more_subtrees/__init__.py
```
