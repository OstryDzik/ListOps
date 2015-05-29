from src.utils import UnsupportedOperation


class List():
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __add__(self, other):
        return List(self.value + other.value)

    def __sub__(self, other):
        raise UnsupportedOperation("You can't subtract two lists!")

    def __mul__(self, other):
        raise UnsupportedOperation("You can't multiply two lists!")

    def __truediv__(self, other):
        raise UnsupportedOperation("You can't divide two lists!")

    def __mod__(self, other):
        raise UnsupportedOperation("You can't modulo two lists!")

    def __ge__(self, other):
        raise UnsupportedOperation("You can't compare two lists with >= !")

    def __gt__(self, other):
        raise UnsupportedOperation("You can't compare two lists with > !")

    def __le__(self, other):
        raise UnsupportedOperation("You can't compare two lists with <=!")

    def __lt__(self, other):
        raise UnsupportedOperation("You can't compare two lists with <!")

    def get_value(self):
        return self



class Identifier():
    value = ""
    def __init__(self, value, memory=None):
        self.value = value
        self.memory = memory

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def get_value(self):
        return self.memory.get_variable_value(self)


