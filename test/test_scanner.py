import unittest

from src.tokens import TokenType, Token
from src.scanner import Scanner
from src.utils import TokenMismatchException, EOF


class NumberScannerTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_integer(self):
        input = "432"
        scanner = Scanner(input)
        self.assertEqual(scanner._read_integer(), "432")

    def test_fail_to_read_integer(self):
        input = "0432"
        scanner = Scanner(input)
        self.assertRaises(TokenMismatchException, lambda: scanner._read_integer())

    def test_fail_to_read_no_digits_after_minus(self):
        input = "-"
        scanner = Scanner(input)
        self.assertRaises(TokenMismatchException, lambda: scanner._read_integer())

    def test_fail_to_read_alfa(self):
        input = "abc"
        scanner = Scanner(input)
        self.assertRaises(TokenMismatchException, lambda: scanner._read_integer())

    def test_read_float_value(self):
        input = ".432"
        scanner = Scanner(input)
        self.assertEqual(scanner._read_float_value(), ".432")

    def test_fail_to_read_float_value_after_comma(self):
        input = "."
        scanner = Scanner(input)
        self.assertRaises(TokenMismatchException, lambda: scanner._read_float_value())

    def test_fail_to_read_float_value(self):
        input = "432"
        scanner = Scanner(input)
        self.assertRaises(TokenMismatchException, lambda: scanner._read_float_value())

    def test_try_to_read_integer(self):
        input = "432"
        scanner = Scanner(input)
        scanner._try_number()
        self.assertEqual(scanner.get_token(), Token(TokenType.integer, "432"))

    def test_try_to_read_float(self):
        input = "432.234"
        scanner = Scanner(input)
        scanner._try_number()
        self.assertEqual(scanner.get_token(), Token(TokenType.float, "432.234"))

    def test_try_to_read_two_floats(self):
        input = "432.234  55.51"
        scanner = Scanner(input)
        t1 = scanner.read_next_token()
        t2 = scanner.read_next_token()
        self.assertEqual(t1, Token(TokenType.float, "432.234"))
        self.assertEqual(t2, Token(TokenType.float, "55.51"))


class OperatorScannerTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_one_char(self):
        input = ")"
        scanner = Scanner(input)
        self.assertEqual(scanner._read_one_char(")"), ")")

    def test_read_one_char_wrong_doesnt_advance_position(self):
        input = "!"
        scanner = Scanner(input)
        starting_pos = scanner.position
        try:
            scanner._read_one_char(".")
        except TokenMismatchException as e:
            pass
        current_pos = scanner.position
        self.assertEqual(starting_pos, current_pos)

    def test_try_lparent(self):
        input = "("
        scanner = Scanner(input)
        scanner._try_lparent()
        self.assertEqual(scanner.get_token(), Token(TokenType.lparent, "("))

    def test_try_rparent(self):
        input = ")"
        scanner = Scanner(input)
        scanner._try_rparent()
        self.assertEqual(scanner.get_token(), Token(TokenType.rparent, ")"))

    def test_try_rbrace(self):
        input = "}"
        scanner = Scanner(input)
        scanner._try_rbrace()
        self.assertEqual(scanner.get_token(), Token(TokenType.rbrace, "}"))

    def test_try_lbrace(self):
        input = "{"
        scanner = Scanner(input)
        scanner._try_lbrace()
        self.assertEqual(scanner.get_token(), Token(TokenType.lbrace, "{"))

    def test_try_rsquare(self):
        input = "]"
        scanner = Scanner(input)
        scanner._try_rsquare()
        self.assertEqual(scanner.get_token(), Token(TokenType.rsquare, "]"))

    def test_try_lsquare(self):
        input = "["
        scanner = Scanner(input)
        scanner._try_lsquare()
        self.assertEqual(scanner.get_token(), Token(TokenType.lsquare, "["))

    def test_try_not_sign(self):
        input = "!"
        scanner = Scanner(input)
        scanner._try_not_sign()
        self.assertEqual(scanner.get_token(), Token(TokenType.notSign, "!"))

    def test_try_assign_operator(self):
        input = "="
        scanner = Scanner(input)
        scanner._try_assign_operator()
        self.assertEqual(scanner.get_token(), Token(TokenType.assignOperator, "="))

    def test_try_fail_assign_operator(self):
        input = "=="
        scanner = Scanner(input)
        self.assertRaises(TokenMismatchException, lambda: scanner._try_assign_operator())

    def test_try_comma(self):
        input = ","
        scanner = Scanner(input)
        scanner._try_comma()
        self.assertEqual(scanner.get_token(), Token(TokenType.comma, ","))

    def test_try_dot(self):
        input = "."
        scanner = Scanner(input)
        scanner._try_dot()
        self.assertEqual(scanner.get_token(), Token(TokenType.dot, "."))

    def test_try_range_operator(self):
        input = ":"
        scanner = Scanner(input)
        scanner._try_range_operator()
        self.assertEqual(scanner.get_token(), Token(TokenType.rangeOperator, ":"))

    def test_try_map_operator(self):
        input = "->"
        scanner = Scanner(input)
        scanner._try_map_operator()
        self.assertEqual(scanner.get_token(), Token(TokenType.mapOperator, "->"))

    def test_try_fail_map_operator(self):
        input = "-!"
        scanner = Scanner(input)
        starting_pos = scanner.position
        self.assertRaises(TokenMismatchException, lambda: scanner._try_map_operator())
        current_pos = scanner.position
        self.assertEqual(starting_pos, current_pos)

    def test_try_top_logic_operator(self):
        input = "||"
        scanner = Scanner(input)
        scanner._try_top_logic_operator()
        self.assertEqual(scanner.get_token(), Token(TokenType.topLogicOperator, "||"))

    def test_try_bot_logic_operator(self):
        input = "&&"
        scanner = Scanner(input)
        scanner._try_bot_logic_operator()
        self.assertEqual(scanner.get_token(), Token(TokenType.botLogicOperator, "&&"))

    def test_try_bot_operator(self):
        input = "+"
        scanner = Scanner(input)
        scanner._try_bot_operator()
        self.assertEqual(scanner.get_token(), Token(TokenType.botOperator, "+"))

    def test_try_test_operator(self):
        input = "<<=!==="
        scanner = Scanner(input)
        scanner._try_test_operator()
        self.assertEqual(scanner.get_token(), Token(TokenType.testOperator, "<"))
        scanner._try_test_operator()
        self.assertEqual(scanner.get_token(), Token(TokenType.testOperator, "<="))
        scanner._try_test_operator()
        self.assertEqual(scanner.get_token(), Token(TokenType.testOperator, "!="))
        scanner._try_test_operator()
        self.assertEqual(scanner.get_token(), Token(TokenType.testOperator, "=="))

    def test_try_test_operator_fails_and_rewinds(self):
        input = "=!"
        scanner = Scanner(input)
        pos = scanner.position
        self.assertRaises(TokenMismatchException, lambda: scanner._try_test_operator())
        pos2 = scanner.position
        self.assertEqual(pos, pos2)

    def test_try_EOF(self):
        input = ""
        scanner = Scanner(input)
        scanner._try_EOF()
        self.assertEqual(scanner.get_token(), Token(TokenType.EOF, EOF))


class StringScannerTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_try_read_id(self):
        input = "abcds_321_dbca"
        scanner = Scanner(input)
        scanner._try_string()
        self.assertEqual(scanner.get_token(), Token(TokenType.id, "abcds_321_dbca"))

    def test_read_alfa_string(self):
        input = "abcds_321_dbca"
        scanner = Scanner(input)
        self.assertEqual(scanner._read_alfa_string(), "abcds_321_dbca")

    def test_fail_read_string(self):
        input = "1bcds_321_dbca"
        scanner = Scanner(input)
        self.assertRaises(TokenMismatchException, lambda: scanner._read_alfa_string())

    def test_read_keyword(self):
        input = "for"
        scanner = Scanner(input)
        self.assertEqual(scanner._read_keyword(input), "for")

    def test_try_keyword(self):
        input = "for"
        scanner = Scanner(input)
        scanner._try_string()
        self.assertEqual(scanner.get_token(), Token(TokenType.keyword, "for"))

    def test_peek_token(self):
        input = "for+2"
        scanner = Scanner(input)
        scanner.read_next_token()
        token1 = scanner.peek_token()
        token2 = scanner.read_next_token()
        self.assertEqual(token1, Token(TokenType.botOperator, "+"))
        self.assertEqual(token1, Token(TokenType.botOperator, "+"))