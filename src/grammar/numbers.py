class Literal():
    value = 0
    value_as_string = ""

    def get_value(self):
        return self

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __add__(self, other):
        return Number(self.value + other.value)

    def __sub__(self, other):
        return Number(self.value - other.value)

    def __mul__(self, other):
        return Number(self.value * other.value)

    def __truediv__(self, other):
        return Number(self.value / other.value)

    def __mod__(self, other):
        return Number(self.value % other.value)

    def __ge__(self, other):
        return self.value >= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __lt__(self, other):
        return self.value < other.value

    def __index__(self):
        return self.value

    def __repr__(self):
        return self.value_as_string

    def __len__(self):
        return Number(1)

    def call_function(self, func):
        return func.call(self)


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
        try:
            self.value = signed_number.value
            self.value_as_string = signed_number.value_as_string
        except AttributeError:
            self.value = signed_number
            self.value_as_string = str(signed_number)