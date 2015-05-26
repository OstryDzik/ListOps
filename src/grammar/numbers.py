class Literal():
    value = 0
    value_as_string = ""

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__


class Integer(Literal):
    def __init__(self, value):
        self.value_as_string = value
        self.value = int(value)


class Float(Literal):
    def __init__(self, value):
        self.value_as_string = value
        self.value = float(value)


class SignedInteger(Literal):
    def __init__(self, integer, sign=""):
        if sign == "":
            self.value = integer.value
            self.value_as_string = integer.value_as_string
        else:
            self.value_as_string = sign + integer.value_as_string
            self.value = int(self.value_as_string)


class SignedFloat(Literal):
    def __init__(self, number, sign=""):
        if sign == "":
            self.value = number.value
            self.value_as_string = number.value_as_string
        else:
            self.value_as_string = sign + number.value_as_string
            self.value = float(self.value_as_string)


class Number(Literal):
    def __init__(self, signed_number):
        self.value = signed_number.value
        self.value_as_string = signed_number.value_as_string