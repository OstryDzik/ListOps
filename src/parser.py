from src.grammar.numbers import Integer, SignedInteger, Float, SignedFloat, Number
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
                "Expected token of type {0}, got {1} with value ".format(type, token.type, token.value))
        if value != "" and token.value != value:
            raise UnexpectedToken("Expected token of value {0}, got {1}".format(value, token.value))
        return token

    def _check_token_type(self, type):
        return self.scanner.get_token().type == type

    ## readers

    def _read_integer(self):
        try:
            value = self._require_token(TokenType.integer).value
        except UnexpectedToken as e:
            raise
        self._advance()
        return Integer(value)

    def _read_signed_integer(self):
        try:
            sign = self._require_token(TokenType.botOperator).value
            self._advance()
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
        self._advance()
        return Float(value)

    def _read_signed_float(self):
        try:
            sign = self._require_token(TokenType.botOperator).value
            self._advance()
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
            signed = self._read_signed_float()
            return Number(signed)
        except UnexpectedToken:
            pass
        try:
            signed = self._read_signed_integer()
            return Number(signed)
        except UnexpectedToken as e:
            raise
