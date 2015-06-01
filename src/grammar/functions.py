from src.grammar.identifier import Identifier
from src.grammar.list import List
from src.grammar.numbers import Number
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
        self.id.register_variable(None)

    def __eq__(self, other):
        return self.id == other.id and self.expr == other.expr

    def __ne__(self, other):
        return self.id != other.id or self.expr != other.expr

    def get_value(self, value):
        self.id.update_variable(value)
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
        return Number(len(value))


class PrintFunction():
    def __init__(self, args):
        if args is not None:
            raise ParseException("Wrong arguments for print function!")
        pass

    def call(self, value):
        print(value)
        return List(value)


class SliceFunction():
    def __init__(self, largument=None, rargument=None, indexOnly=False):
        self.larg = largument
        self.rarg = rargument
        self.indexOnly = indexOnly

    def call(self, value):
        if isinstance(self.larg, Identifier):
            self.larg == self.larg.get_value()
        if isinstance(self.rarg, Identifier):
            self.rarg == self.rarg.get_value()
        try:
            if self.indexOnly:
                return List(value[self.larg.get_value()])
            if self.larg is None and self.rarg is None:
                return (List(value[:]))
            if self.larg is None:
                return (List(value[:self.rarg.get_value()]))
            if self.rarg is None:
                return (List(value[self.larg.get_value():]))
            return (List(value[self.larg.get_value():self.rarg.get_value()]))
        except AttributeError:
            raise ParseException("Wrong slice operator call!")

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

