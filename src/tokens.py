from enum import Enum


class TokenType(Enum):
    lparent = "lparent"
    rparent = "rparent"
    lbrace = "lbrace"
    rbrace = "rabrace"
    lsquare = "lsquare"
    rsquare = "rsquare"
    id = "id"
    integer = "integer"
    float = "float"
    topOperator = "topOperator"
    botOperator = "botOperator"
    testOperator = "testOperator"
    botLogicOperator = "botLogicOperator"
    topLogicOperator = "topLogicOperator"
    notSign = "notSign"  # !
    keyword = "keyword"  #
    comma = "comma"  # ,
    dot = "dot"  # .
    mapOperator = "mapOperator"  # ->
    assignOperator = "assignOperator"  # =
    rangeOperator = "rangeOperator"
    EOF = "EOF"


class Token():
    def __init__(self, type, val):
        self.type = type
        self.value = val

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def print(self):
        print(self.type.value + ": " + self.value)
