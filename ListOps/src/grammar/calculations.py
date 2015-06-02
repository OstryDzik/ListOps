from enum import Enum

from ListOps.src.utils import ParseException


class CalcType(Enum):
    topCalc = 0,
    calc = 1


class Calculation():
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
        if self.type == CalcType.calc:
            if self.operator == '+':
                return loperand + roperand
            if self.operator == '-':
                return loperand - roperand
        elif self.type == CalcType.topCalc:
            if self.operator == '*':
                return loperand * roperand
            if self.operator == '/':
                return loperand / roperand
            if self.operator == '%':
                return loperand % roperand
        else:
            raise ParseException("Wrong calc type!")