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

