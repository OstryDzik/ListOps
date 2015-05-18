class Token():
    def __init__(self, val):
        self.value = val


class Keyword(Token):
    def print(self):
        print("Keyword " + self.value)


class AlphaString(Token):
    def print(self):
        print("AlphaString " + self.value)


class NumString(Token):
    def print(self):
        print("NumString " + self.value)


class Operator(Token):
    def print(self):
        print("Operator " + self.value)


class Parenthesis(Token):
    def print(self):
        print("Parenthesis " + self.value)


class Braces(Token):
    def print(self):
        print("Braces " + self.value)