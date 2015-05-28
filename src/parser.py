from src.grammar.numbers import Integer, SignedInteger, Float, SignedFloat, Number
from src.grammar.objects import Identifier
from src.tokens import TokenType
from src.utils import UnexpectedToken, EOFException


class Parser():
    def __init__(self, scanner):
        self.scanner = scanner

    def parse(self):
        return

    ## helper methods

    def _advance(self):
        try:
            self.scanner.read_next_token()
        except EOFException:
            print("Encountered end of input")

    def _require_token(self, type, value=""):
        token = self.scanner.get_token()
        if token.type != type:
            raise UnexpectedToken(
                "Error at position {3}: Expected token of type {0}, got {1} with value {2}".format(type, token.type,
                                                                                                   token.value, str(
                        self.scanner.get_position())))
        if value != "" and token.value != value:
            raise UnexpectedToken(
                "Error at position {4}: Expected token type {2} of value {0}, got {1}".format(value, token.value,
                                                                                              token.type, str(
                        self.scanner.get_position())))
        self._advance()
        return token

    def _check_token_type(self, type):
        return self.scanner.get_token().type == type

    ## readers

    def _read_integer(self):
        try:
            value = self._require_token(TokenType.integer).value
        except UnexpectedToken as e:
            raise
        return Integer(value)

    def _read_signed_integer(self):
        try:
            sign = self._require_token(TokenType.botOperator).value
        except UnexpectedToken:
            sign = ""
            pass
        try:
            number = self._read_integer()
        except UnexpectedToken as e:
            raise
        return SignedInteger(number, sign)

    def _read_float(self):
        try:
            value = self._require_token(TokenType.float).value
        except UnexpectedToken as e:
            raise
        return Float(value)

    def _read_signed_float(self):
        try:
            sign = self._require_token(TokenType.botOperator).value
        except UnexpectedToken:
            sign = ""
            pass
        try:
            number = self._read_float()
        except UnexpectedToken as e:
            raise
        return SignedFloat(number, sign)

    def _read_number(self):
        try:
            sign = self._require_token(TokenType.botOperator).value
        except UnexpectedToken:
            sign = ""
            pass
        try:
            number = SignedFloat(self._read_float(), sign)
            return Number(number)
        except UnexpectedToken as e:
            pass
        try:
            number = SignedInteger(self._read_integer(), sign)
        except UnexpectedToken as e:
            raise
        return Number(number)


    def _read_identifier(self):
        try:
            id = self._require_token(TokenType.id)
        except UnexpectedToken:
            raise
        return Identifier(id.value)

    def _read_list_of_elements(self):
        list = []
        try:  # check for left brace
            self._require_token(TokenType.lbrace)
        except UnexpectedToken as e:
            raise
        try:  # empty braces?
            self._require_token(TokenType.rbrace)
        except UnexpectedToken as e:
            pass  # no problem
        while (True):  # read numbers
            try:
                num = self._read_number()
                list.append(num.value)
            except UnexpectedToken as e:
                raise
            if self._check_token_type(TokenType.rbrace):
                break
            try:  # read comma
                self._require_token(TokenType.comma)
            except UnexpectedToken as e:
                raise
            if self._check_token_type(TokenType.rbrace):  # brace ofter comma? wrong
                raise UnexpectedToken(
                    "Error at position {0} ,Expected number after comma".format(str(self.scanner.get_position())))
        try:  # check for ending brace
            self._require_token(TokenType.rbrace)
        except UnexpectedToken as e:
            raise
        return list