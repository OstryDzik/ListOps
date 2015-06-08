import unittest

from ListOps.src.grammar.assignment import Assignment, Declaration
from ListOps.src.grammar.calculations import Calculation
from ListOps.src.grammar.cust_functions import Function, FunctionDefinition
from ListOps.src.grammar.for_loop import ForLoop
from ListOps.src.grammar.sys_functions import FunctionExpr, FilterFunction, FuncCall, SliceFunction
from ListOps.src.grammar.if_statement import IfStatement
from ListOps.src.grammar.logic_test import LogicTest
from ListOps.src.grammar.numbers import Integer, Float, SignedFloat, SignedInteger, Number
from ListOps.src.grammar.list import List
from ListOps.src.grammar.identifier import Identifier
from ListOps.src.parser import Parser
from ListOps.src.scanner import Scanner
from ListOps.src.tokens import Token, TokenType
from ListOps.src.utils import UnexpectedToken, UnsupportedOperation, RunError


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
        ref_list = List([Number(12), Number(-3), Number(12.42), Number(-31.21), Number(41)])
        self.assertEqual(list, ref_list)

    def test_read_list_of_one_number(self):
        value = "{12}"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        list = parser._read_list_of_numbers()
        ref_list = List([Number(12)])
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
        ref_list = [Number(12), Number(-3), Identifier("a"), Identifier("b")]
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
        list = [Number(12), Number(-3), Identifier("a"), Identifier("b")]
        self.assertEqual(list, parser._read_arguments_list())


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
        self.assertEqual(value, Number(32))


    def test_read_two_top_calcs(self):
        input = "4*8/2"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        value = parser._read_top_calc().get_value()
        self.assertEqual(value, Number(16))

    def test_read_bot_calc(self):
        input = "4+8"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        value = parser._read_calc().get_value()
        self.assertEqual(value, Number(12))

    def test_read_single_arg_calc(self):
        input = "4"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        value = parser._read_calc().get_value()
        self.assertEqual(value, Number(4))

    def test_read_calc_with_proper_operator_priority(self):
        input = "4+8*2"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        value = parser._read_calc().get_value()
        self.assertEqual(value, Number(20))

    def test_read_calc_with_proper_reversed_operator_priority(self):
        input = "4*8+2"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        value = parser._read_calc().get_value()
        self.assertEqual(value, Number(34))

    def test_read_calc_with_proper_parenthesis(self):
        input = "((4+8)*2)/12"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        value = parser._read_calc().get_value()
        self.assertEqual(value, Number(2))

    def test_read_calc_with_variables(self):
        input = "a+b"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser.memory.register_variable(Identifier("a"), List([1, 2, 3]))
        parser.memory.register_variable(Identifier("b"), List([4, 5, 6]))
        parser._advance()
        calc = parser._read_calc()
        self.assertEqual(calc.get_value(), List([1, 2, 3, 4, 5, 6]))

    def test_read_illegal_calc(self):
        input = "a-b"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser.memory.register_variable(Identifier("a"), List([1, 2, 3]))
        parser.memory.register_variable(Identifier("b"), List([4, 5, 6]))
        parser._advance()
        calc = parser._read_calc()
        self.assertRaises(RunError, lambda: calc.get_value())

    def test_read_test_arg(self):
        input = "4>8"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        value = parser._read_test_argument().get_value()
        self.assertEqual(value, False)

    def test_read_bot_logic_test(self):
        input = "4>8 || 3<4"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        value = parser._read_logic_test().get_value()
        self.assertEqual(value, True)

    def test_read_top_logic_test(self):
        input = "4>8 && 3<4"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        value = parser._read_top_logic_test().get_value()
        self.assertEqual(value, False)

    def test_logic_operator_hierachy(self):
        input = "10>8 || 3<4 && 8>9"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        value = parser._read_logic_test().get_value()
        self.assertEqual(value, True)
        input = "7>8 || 3<4 && 10>9"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        value = parser._read_logic_test().get_value()
        self.assertEqual(value, True)

    def test_read_logic_test_with_proper_parenthesis(self):
        input = "(10>8 || (3<4 && 8>9))"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        value = parser._read_logic_test().get_value()
        self.assertEqual(value, True)


class ParserFunctionsTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_func_expr_calc_test(self):
        input = "a->a+2"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        expr = parser._read_func_expr()
        self.assertEqual(expr.get_value(Number(5)), Number(7))

    def test_read_func_expr_logic_test(self):
        input = "a->a>2"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        expr = parser._read_func_expr()
        self.assertEqual(expr.get_value(Number(1)), False)

    def test_read_sys_func_args(self):
        input = "(a->a>2)"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        expr = parser._read_sys_func_args()
        self.assertEqual(isinstance(expr, FunctionExpr), True)

    def test_read_empty_sys_func_args(self):
        input = "()"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        expr = parser._read_sys_func_args()
        self.assertEqual(expr, None)

    def test_read_sys_func(self):
        input = "filter(a->a>2)"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        func = parser._read_sys_func()
        self.assertEqual(isinstance(func, FilterFunction), True)

    def test_read_sys_func_call(self):
        input = "a.filter(a->a>2)"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        func = parser._read_sys_func_call()
        self.assertEqual(isinstance(func, FuncCall), True)

    def test_execute_sys_func_call(self):
        input = "a.filter(a->a>2)"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser.memory.register_variable(Identifier("a"), List([Number(1), Number(2), Number(3), Number(4), Number(5)]))
        parser._advance()
        func = parser._read_sys_func_call()
        self.assertEqual(func.get_value(), List([Number(3), Number(4), Number(5)]))

    def test_execute_chain_sys_func_call(self):
        input = "a.filter(a->a>2).map(a->a+1)"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser.memory.register_variable(Identifier("a"), List([Number(1), Number(2), Number(3), Number(4), Number(5)]))
        parser._advance()
        func = parser._read_sys_func_call()
        self.assertEqual(func.get_value(), List([Number(4), Number(5), Number(6)]))

    def test_read_slice(self):
        input = "[1:2]"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        slice = parser._read_slice()
        self.assertEqual(isinstance(slice, SliceFunction), True)
        input = "[1:]"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        slice = parser._read_slice()
        self.assertEqual(isinstance(slice, SliceFunction), True)
        input = "[:2]"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        slice = parser._read_slice()
        self.assertEqual(isinstance(slice, SliceFunction), True)
        input = "[:]"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        slice = parser._read_slice()
        self.assertEqual(isinstance(slice, SliceFunction), True)
        input = "[a:2]"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        slice = parser._read_slice()
        self.assertEqual(isinstance(slice, SliceFunction), True)
        input = "[2]"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        slice = parser._read_slice()
        self.assertEqual(isinstance(slice, SliceFunction), True)

    def test_read_slice_call(self):
        input = "a[1:2]"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        slice = parser._read_slice_call()
        self.assertEqual(isinstance(slice, FuncCall), True)


    def test_read_cust_func_call(self):
        input = "a(b, c)"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        func = parser._read_cust_func_call()
        self.assertEqual(isinstance(func, Function), True)

    def test_read_return_statement(self):
        input = "return e"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        ret = parser._read_return_statement()
        self.assertEqual(isinstance(ret, Identifier), True)

    def test_read_cust_func_body(self):
        input = """
        {
            b.print()
            a.print()
            return a
        }"""
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        ret = parser._read_cust_function_body()
        self.assertEqual(isinstance(ret[0], list), True)
        self.assertEqual(isinstance(ret[1], Identifier), True)

    def test_read_cust_func_definition(self):
        input = """
        def x(a,b,c)
        {
            b.print()
            a.print()
            return a
        }"""
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        func = parser._read_cust_function_definition()
        self.assertEqual(isinstance(func, FunctionDefinition), True)


class ParserVariablesTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_variable_assignment(self):
        input = "a=2+2"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        expr = parser._read_assignment()
        self.assertEqual(isinstance(expr, Assignment), True)
        self.assertEqual(isinstance(expr.value, Calculation), True)
        input = "a=b[2:18]"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        expr = parser._read_assignment()
        self.assertEqual(isinstance(expr.value, FuncCall), True)
        input = "a=b.map(c->14)"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        expr = parser._read_assignment()
        self.assertEqual(isinstance(expr.value, FuncCall), True)

    def test_list_element_assignment(self):
        input = "a[3]=2+2"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        expr = parser._read_assignment()
        self.assertEqual(isinstance(expr, Assignment), True)
        self.assertEqual(isinstance(expr.value, Calculation), True)

    def test_variable_declaration(self):
        input = "var a=2+2"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        expr = parser._read_declaration()
        self.assertEqual(isinstance(expr, Declaration), True)
        input = "var a"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        expr = parser._read_declaration()
        self.assertEqual(isinstance(expr, Declaration), True)


class ParserForTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_wrong_for_header(self):
        value = "(a in b : )"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        self.assertRaises(UnexpectedToken, lambda: parser._read_for_loop_header())

    def test_read_for_header(self):
        value = "(a in b)"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        header = parser._read_for_loop_header()
        self.assertEqual(header['id'], Identifier('a'))
        self.assertEqual(header['list'], Identifier('b'))
        self.assertEqual(header['test'], None)

    def test_read_for_body(self):
        value = "{a=12}"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        body = parser._read_body()
        self.assertEqual(isinstance(body, list), True)

    def test_read_for_loop(self):
        value = "for (a in b : a>4){a=a+1}"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        loop = parser._read_for_loop()
        self.assertEqual(isinstance(loop, ForLoop), True)


class ParserIfTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_if_header(self):
        value = "(a>4)"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        header = parser._read_if_header()
        self.assertEqual(isinstance(header, LogicTest), True)

    def test_read_if_body(self):
        value = "if(a>4){a=12}"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        header = parser._read_if_statement()
        self.assertEqual(isinstance(header, IfStatement), True)

    def test_read_if_else_statement(self):
        value = "if(a>4){a=12}else{a=15}"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        header = parser._read_if_statement()
        self.assertEqual(isinstance(header, IfStatement), True)
        self.assertEqual(isinstance(header.alt_expr, list), True)


class ParserComplexTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse(self):
        value = "if(a>4){a=12}else{a=15}"
        scanner = Scanner(value)
        parser = Parser(scanner)
        statements = parser.parse()
        self.assertEqual(len(statements.statements), 1)

    def test_parse_combined_statements(self):
        value = """if(a>4){a=12}else{a=15}
                    for (a in b : a>4){a=a+1}
                    a=2+2
                    var a=2+2
                    """
        scanner = Scanner(value)
        parser = Parser(scanner)
        statements = parser.parse()
        self.assertEqual(len(statements.statements), 4)