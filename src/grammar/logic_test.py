from enum import Enum
from src.utils import ParseException


class TestType(Enum):
    topTest = 0,
    botTest = 1


class LogicTest():
    def __init__(self, type, loperand, operator=None, roperand=None):
        self.type = type
        self.loperand = loperand
        self.operator = operator
        self.roperand = roperand

    def get_value(self):
        if self.operator is None and self.roperand is None:
            return self.loperand.get_value()
        else:
            lop = self.loperand.get_value()
            rop = self.roperand.get_value()
            return self.calculate(lop, rop)

    def calculate(self, loperand, roperand):
        if self.type == TestType.botTest:
            if self.operator == '&&':
                return loperand and roperand
        elif self.type == TestType.topTest:
            if self.operator == '||':
                return loperand or roperand
        else:
            raise ParseException("Wrong test type!")


class TestArgument():
    def __init__(self, loperand, operator=None, roperand=None):
        self.loperand = loperand
        self.operator = operator
        self.roperand = roperand

    def get_value(self):
        if self.roperand is None:
            if self.operator is None:
                return self.loperand.get_value()
            if self.operator == "!":
                return not self.loperand.get_value()
            else:
                raise ParseException("Wrong test type!")
        else:
            lop = self.loperand.get_value()
            rop = self.roperand.get_value()
            return self.calculate(lop, rop)

    def calculate(self, loperand, roperand):
        if self.operator == '==':
            return loperand == roperand
        if self.operator == '>':
            return loperand > roperand
        if self.operator == '<':
            return loperand < roperand
        if self.operator == '<=':
            return loperand <= roperand
        if self.operator == '>=':
            return loperand >= roperand
        if self.operator == '!=':
            return loperand != roperand
        raise ParseException("Wrong test type!")