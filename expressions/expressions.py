"""Implements an expression tree class hierarchy."""
import numbers


class Expression:
    """Expression class."""

    def __init__(self, precedence, tuple=()):
        """Define constructor."""
        self.operands = tuple
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
        if self.operands[0].precedence < self.precedence:
            string1 = f"({str(self.operands[0])})"
        else:
            string1 = f"{str(self.operands[0])}"
        if self.operands[1].precedence < self.precedence:
            string2 = f"({str(self.operands[1])})"
        else:
            string2 = f"{str(self.operands[1])}"
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
