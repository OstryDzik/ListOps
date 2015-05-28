from enum import Enum


class Identifier():
    value = ""

    def __init__(self, value, memory=None):
        self.value = value
        self.memory = memory

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def get_value(self):
        return self.memory.get_variable_value(self)


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
            return {
                '+': loperand + roperand,
                '-': loperand - roperand
            }[self.operator]
        else:
            return {
                '*': loperand * roperand,
                '/': loperand - roperand,
                '%': loperand % roperand
            }[self.operator]