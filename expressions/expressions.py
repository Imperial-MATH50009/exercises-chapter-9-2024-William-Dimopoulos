"""Implements an expression tree class hierarchy."""
import numbers
from functools import singledispatch


class Expression:
    """Expression class."""

    def __init__(self, precedence, o=()):
        """Define constructor."""
        operands = list(o)
        for n in range(len(operands)):
            if isinstance(operands[n], int):
                operands[n] = Number(operands[n])
        self.operands = tuple(operands)
        self.precedence = precedence

    def __add__(self, other):
        """Define addition."""
        if isinstance(other, numbers.Number):
            return Add(self, Number(other))
        else:
            return Add(self, other)

    def __radd__(self, other):
        """Define reverse addition."""
        if isinstance(other, numbers.Number):
            return Add(Number(other), self)
        else:
            return Add(other, self)

    def __sub__(self, other):
        """Define subtraction."""
        if isinstance(other, numbers.Number):
            return Sub(self, Number(other))
        else:
            return Sub(self, other)

    def __rsub__(self, other):
        """Define reverse subtraction."""
        if isinstance(other, numbers.Number):
            return Sub(Number(other), self)
        else:
            return Sub(other, self)

    def __mul__(self, other):
        """Define addition."""
        if isinstance(other, numbers.Number):
            return Mul(self, Number(other))
        else:
            return Mul(self, other)

    def __rmul__(self, other):
        """Define reverse addition."""
        if isinstance(other, numbers.Number):
            return Mul(Number(other), self)
        else:
            return Mul(other, self)

    def __truediv__(self, other):
        """Define addition."""
        if isinstance(other, numbers.Number):
            return Div(self, Number(other))
        else:
            return Div(self, other)

    def __rtruediv__(self, other):
        """Define reverse addition."""
        if isinstance(other, numbers.Number):
            return Div(Number(other), self)
        else:
            return Div(other, self)

    def __pow__(self, other):
        """Define addition."""
        if isinstance(other, numbers.Number):
            return Pow(self, Number(other))
        else:
            return Pow(self, other)

    def __rpow__(self, other):
        """Define reverse addition."""
        if isinstance(other, numbers.Number):
            return Pow(Number(other), self)
        else:
            return Pow(other, self)


class Operator(Expression):
    """Operator subclass."""

    def __repr__(self):
        """Define canonical string representation."""
        return type(self).__name__ + repr(self.operands)

    def __str__(self):
        """Define string representation."""
        if isinstance(self.operands[0], int) or \
                self.operands[0].precedence >= self.precedence:
            string1 = f"{str(self.operands[0])}"
        else:
            string1 = f"({str(self.operands[0])})"
        if isinstance(self.operands[1], int) or \
                self.operands[1].precedence >= self.precedence:
            string2 = f"{str(self.operands[1])}"
        else:
            string2 = f"({str(self.operands[1])})"
        return string1 + f" {self.symbol} " + string2


class Add(Operator):
    """Operator subclass."""

    def __init__(self, first, second):
        """Define constructor."""
        super().__init__(1, (first, second))
        self.symbol = "+"


class Sub(Operator):
    """Operator subclass."""

    def __init__(self, first, second):
        """Define constructor."""
        super().__init__(1, (first, second))
        self.symbol = "-"


class Mul(Operator):
    """Operator subclass."""

    def __init__(self, first, second):
        """Define constructor."""
        super().__init__(2, (first, second))
        self.symbol = "*"


class Div(Operator):
    """Operator subclass."""

    def __init__(self, first, second):
        """Define constructor."""
        super().__init__(2, (first, second))
        self.symbol = "/"


class Pow(Operator):
    """Operator subclass."""

    def __init__(self, first, second):
        """Define constructor."""
        super().__init__(3, (first, second))
        self.symbol = "^"


class Terminal(Expression):
    """Terminal subclass."""

    def __init__(self, value):
        """Define class constructor."""
        self.value = value
        super().__init__(precedence=float("inf"))

    def __repr__(self):
        """Define canonical string representation."""
        return repr(self.value)

    def __str__(self):
        """Define string representation."""
        return str(self.value)


class Number(Terminal):
    """Number subclass."""

    def __init__(self, value):
        """Define constructor."""
        if not isinstance(value, numbers.Number):
            raise TypeError("Value must be a number.")
        else:
            super().__init__(value)


class Symbol(Terminal):
    """Symbol subclass."""

    def __init__(self, value):
        """Define constructor."""
        if not isinstance(value, str):
            raise TypeError("Value must be a string.")
        else:
            super().__init__(value)


def postvisitor(expr, fn, **kwargs):
    """Visit an expression in postorder applying a function to every node."""
    stack = []
    visited = {}

    stack.append(expr)
    while stack:
        e = stack.pop()
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


@singledispatch
def differentiate(expr, o=(), **kwags):
    """Differentiate an expression node."""
    raise NotImplementedError(f"Cannot evaluate a {type(expr).__name__}")


@differentiate.register(Number)
def _(expr, **kwags):
    return Number(0)


@differentiate.register(Symbol)
def _(expr, *o, **kwags):
    if expr.value == kwags["var"]:
        return Number(1.)
    else:
        return Number(0.)


@differentiate.register(Add)
def _(expr, *o, **kwags):
    return Add(o[0], o[1])


@differentiate.register(Sub)
def _(expr, *o, **kwags):
    return Sub((o[0], o[1]))


@differentiate.register(Mul)
def _(expr, *o, **kwags):
    return Add(Mul(o[0], expr.operands[1]), Mul(o[1], expr.operands[0]))


@differentiate.register(Div)
def _(expr, *o, **kwags):
    return Div(Sub(Mul(o[0], expr.operands[1]), Mul(expr.operands[0], o[1])),
               Pow(expr.operands[1], 2))


@differentiate.register(Pow)
def _(expr, *o, **kwags):
    return Mul(Mul(expr.operands[1], o[0]),
               Pow(expr.operands[0], expr.operands[1]-1))
