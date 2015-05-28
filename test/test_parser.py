import unittest

from src.grammar.numbers import Integer, Float, SignedFloat, SignedInteger, Number
from src.grammar.objects import Identifier
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

    def test_read_id(self):
        value = "abcd"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        id = parser._read_identifier()
        self.assertEqual(id, Identifier(value))

    def test_read_list_of_numbers(self):
        value = "{12,-3,12.42,-31.21,+41}"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        list = parser._read_list_of_numbers()
        ref_list = [12, -3, 12.42, -31.21, 41]
        self.assertEqual(list, ref_list)

    def test_read_list_of_one_number(self):
        value = "{12}"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        list = parser._read_list_of_numbers()
        ref_list = [12]
        self.assertEqual(list, ref_list)

    def test_fail_to_read_list_of_numbers_without_brace(self):
        value = "{12,-3,12.42,-31.21,+41"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        self.assertRaises(UnexpectedToken, lambda: parser._read_list_of_numbers())

    def test_fail_to_read_list_of_numbers_ending_with_comma(self):
        value = "{12,-3,12.42,-31.21,}"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        self.assertRaises(UnexpectedToken, lambda: parser._read_list_of_numbers())

    def test_fail_to_read_list_of_numbers_with_wrong_element(self):
        value = "{12,-3,a,-31.21,}"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        self.assertRaises(UnexpectedToken, lambda: parser._read_list_of_numbers())

    def test_read_element(self):
        value = "b"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        id1 = parser._read_element()
        id = Identifier("b")
        self.assertEqual(id1, id)

    def test_fail_read_element(self):
        value = "}"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        self.assertRaises(UnexpectedToken, lambda: parser._read_element())

    def test_read_list_of_elements(self):
        value = "12,-3,a,b"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        list = parser._read_list_of_elements()
        ref_list = [Number(12, 1), Number(-3, 1), Identifier("a"), Identifier("b")]
        self.assertEqual(list, ref_list)


    def test_fail_to_read_list_of_elements_ending_with_comma(self):
        value = "12,-3,a,b,"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        self.assertRaises(UnexpectedToken, lambda: parser._read_list_of_elements())

    def test_read_args(self):
        value = "(12,-3,a,b)"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        list = [Number(12, 1), Number(-3, 1), Identifier("a"), Identifier("b")]
        self.assertEqual(list, parser._read_arguments())


class ParserCalculationTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_top_calc(self):
        input = "4*8"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        value = parser._read_top_calc().get_value()
        self.assertEqual(value, 32)