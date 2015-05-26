import unittest

from src.grammar.numbers import Integer, Float, SignedFloat, SignedInteger, Number
from src.parser import Parser
from src.scanner import Scanner
from src.tokens import Token, TokenType
from src.utils import UnexpectedToken


class ParserHelperTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_require_token_returns_required_token(self):
        scanner = Scanner("")
        scanner.token = Token(TokenType.lparent, "(")
        parser = Parser(scanner)
        self.assertEqual(parser._require_token(TokenType.lparent), Token(TokenType.lparent, "("))

    def test_require_token_throws_exception_when_token_different_than_required(self):
        scanner = Scanner("")
        scanner.token = Token(TokenType.rparent, ")")
        parser = Parser(scanner)
        self.assertRaises(UnexpectedToken, lambda: parser._require_token(TokenType.lparent))

    def test_require_token_throws_exception_when_value_different_than_required(self):
        scanner = Scanner("")
        scanner.token = Token(TokenType.botOperator, "+")
        parser = Parser(scanner)
        self.assertRaises(UnexpectedToken, lambda: parser._require_token(TokenType.lparent, "-"))

    def test_check_token_type_return_correct_value(self):
        scanner = Scanner("")
        scanner.token = Token(TokenType.lparent, "(")
        parser = Parser(scanner)
        self.assertEqual(parser._check_token_type(TokenType.lparent), True)


class ParserReadTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_integer(self):
        scanner = Scanner("12")
        parser = Parser(scanner)
        parser._advance()
        number = parser._read_integer()
        self.assertEqual(number, Integer("12"))
        self.assertEqual(number.value, 12)

    def test_read_signed_integer(self):
        scanner = Scanner("-12")
        parser = Parser(scanner)
        parser._advance()
        number = parser._read_signed_integer()
        integer = Integer("12")
        self.assertEqual(number, SignedInteger(integer, "-"))
        self.assertEqual(number.value, -12)

    def test_read_float(self):
        scanner = Scanner("12.12")
        parser = Parser(scanner)
        parser._advance()
        number = parser._read_float()
        self.assertEqual(number, Float("12.12"))
        self.assertEqual(number.value, 12.12)

    def test_read_signed_float(self):
        scanner = Scanner("-12.12")
        parser = Parser(scanner)
        parser._advance()
        number = parser._read_signed_float()
        float = Float("12.12")
        self.assertEqual(number, SignedFloat(float, "-"))
        self.assertEqual(number.value, -12.12)

    def test_read_number(self):
        scanner = Scanner("-12.12")
        parser = Parser(scanner)
        parser._advance()
        number = parser._read_number()
        float = Float("12.12")
        signedFloat = SignedFloat(float, "-")
        self.assertEqual(number, Number(signedFloat))