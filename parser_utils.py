from enum import Enum


class VarType(Enum):
    value = "value"
    list = "list"
    func = "func"
    undef = "undef"


class VarValue():
    type = VarType.undef
    value = None

    def __init__(self, type, value):
        type = type
        value = value

    def get_value(self):
        return self.value.value

    def get_type(self):
        return self.type