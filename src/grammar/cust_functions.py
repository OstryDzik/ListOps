from src.grammar.identifier import Identifier
from src.grammar.list import List
from src.utils import ParseException


class FunctionDefinition():
    def __init__(self, id, args, expr, ret):
        self.id = id
        for arg in args:
            if not isinstance(arg, Identifier):
                raise ParseException("Invalid function definition!, please state proper argument list")
        self.args = args
        self.expr = expr
        self.ret = ret

    def call(self, args):
        if len(args) != len(self.args):
            raise ParseException("Invalid function call! Too few arguments stated")
        for i in range(0, len(self.args)):
            self.args[i].update_variable(args[i].get_value())
        for exp in self.expr:
            exp.get_value()
        if self.ret is None:
            return None
        ret_val = self.ret.get_value()
        if isinstance(ret_val, list):
            return List(list)
        return ret_val


    def get_value(self):
        self.id.register_variable(self)
        for arg in self.args:
            arg.register_variable(None)


class Function():
    def __init__(self, id, args):
        self.id = id
        self.args = args

    def get_value(self):
        return self.id.get_value().call(self.args)