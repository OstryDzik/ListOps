from src.grammar.list import List
from src.grammar.numbers import Integer
from src.utils import ParseException


class Function():
    args = {}
    exp = None

    def __init__(self, exp, args):
        for arg in args:
            try:
                self.args[arg.get_name()] = None
            except TypeError:
                raise ParseException("Wrong argument list initialization!")
        self.exp = exp


class FunctionExpr():
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

    def __eq__(self, other):
        return self.id == other.id and self.expr == other.expr

    def __ne__(self, other):
        return self.id != other.id or self.expr != other.expr

    def get_value(self, value):
        self.id.update_value(value)
        return self.expr.get_value()


class MapFunction():
    def __init__(self, args):
        if args is None:
            raise ParseException("Wrong arguments for map function!")
        self.mapping = args

    def call(self, value):
        result = []
        for i in value:
            result.append(self.mapping.get_value(i))
        return List(result)


class FilterFunction():
    def __init__(self, args):
        if args is None:
            raise ParseException("Wrong arguments for filter function!")
        self.test = args

    def call(self, value):
        result = []
        for i in value:
            if self.test.get_value(i):
                result.append(i)
        return List(result)


class LengthFunction():
    def __init__(self, args):
        if args is not None:
            raise ParseException("Wrong arguments for length function!")
        pass

    def call(self, value):
        return Integer(len(value))


class PrintFunction():
    def __init__(self, args):
        if args is not None:
            raise ParseException("Wrong arguments for print function!")
        pass

    def call(self, value):
        print(value)


class FuncCall():
    def __init__(self, who, what):
        self.who = who
        self.what = what

    def get_value(self):
        try:
            caller = self.who.get_value()
            return caller.call_function(self.what)
        except AttributeError:
            return self.who.call_function(self.what)