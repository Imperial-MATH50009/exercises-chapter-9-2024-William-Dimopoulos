"""Postvisitor function."""


def postvisitor(expr, fn, **kwargs):
    """Visit an expression in postorder applying a function to every node."""
    stack = []
    visited = {}

    stack.append(expr)
    while stack:
        e = stack[-1]
        unvisited_children = []
        for o in e.operands:
            if o not in visited:
                unvisited_children.append(o)

        if unvisited_children:
            stack.append(e)
            stack.extend(unvisited_children)
        else:
            visited[e] = fn(e, *(visited[o] for o in e.operands), **kwargs)

    return visited[expr]
