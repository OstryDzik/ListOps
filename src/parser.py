from _elementtree import ParseError
from src.grammar.functions import FunctionExpr, FilterFunction, MapFunction, LengthFunction, PrintFunction, FuncCall
from src.grammar.logic_test import TestArgument, LogicTest, TestType
from src.grammar.numbers import Integer, SignedInteger, Float, SignedFloat, Number
from src.grammar.list import List
from src.grammar.identifier import Identifier
from src.grammar.calculations import CalcType, Calculation
from src.memory import Memory
from src.tokens import TokenType
from src.utils import UnexpectedToken, EOFException, SYS_FUNCS


class Parser():
    def __init__(self, scanner):
        self.scanner = scanner
        self.memory = Memory()

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
                "Error at position {2}: Expected token type {0} , got {1}".format(type, token.type,
                                                                                  str(self.scanner.get_position())))
        if value != "" and token.value != value:
            raise UnexpectedToken(
                "Error at position {3}: Expected token type {2} of value {0}, got {1}".format(value, token.value,
                                                                                              token.type, str(
                        self.scanner.get_position())))
        self._advance()
        return token

    def _check_token_type(self, type):
        return self.scanner.get_token().type == type

    def _get_position(self):
        return self.scanner.get_position()

    def _get_token_type(self):
        return self.scanner.get_token().type

    def _get_token_value(self):
        return self.scanner.get_token().value

    def _raiseUnexpectedToken(self, message):
        raise UnexpectedToken(
            "Error: " + message + " at position {0}, token {1}, value {2}".format(self._get_position(),
                                                                                  self._get_token_type(),
                                                                                  self._get_token_value()))


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
        return Identifier(id.value, self.memory)

    def _read_list_of_numbers(self):
        list = []
        try:  # check for left brace
            self._require_token(TokenType.lbrace)
        except UnexpectedToken as e:
            raise
        try:
            self._require_token(TokenType.rbrace)
            return list
        except UnexpectedToken as e:
            pass
        while (True):
            try:
                num = self._read_number()
                list.append(num.value)
            except UnexpectedToken as e:
                raise
            try:
                self._require_token(TokenType.comma)
            except UnexpectedToken as e:
                break
        try:
            self._require_token(TokenType.rbrace)
        except UnexpectedToken as e:
            raise
        return List(list)

    def _read_element(self):
        elem = None
        try:
            elem = self._read_number()
            return elem
        except UnexpectedToken:
            pass
        try:
            elem = self._read_identifier()
            return elem
        except UnexpectedToken as e:
            raise

    def _read_list_of_elements(self):
        list = []
        while (True):
            try:
                list.append(self._read_element())
            except UnexpectedToken as e:
                raise
            try:
                self._require_token(TokenType.comma)
            except UnexpectedToken:
                break
        return list

    def _read_arguments_list(self):
        list = []
        try:
            self._require_token(TokenType.lparent)
            list += self._read_list_of_elements()
            self._require_token(TokenType.rparent)
        except UnexpectedToken as e:
            raise
        return list

    def _read_calc(self):
        try:
            lop = self._read_top_calc()
        except UnexpectedToken as e:
            raise
        while (True):
            try:
                operator = self._require_token(TokenType.botOperator).value
            except UnexpectedToken:
                return Calculation(CalcType.calc, lop)
            try:
                rop = self._read_top_calc()
            except UnexpectedToken as e:
                raise
            calc = Calculation(CalcType.calc, lop, operator, rop)
            lop = calc

    def _read_top_calc(self):
        try:
            lop = self._read_argument()
        except UnexpectedToken as e:
            raise
        while (True):
            try:
                operator = self._require_token(TokenType.topOperator).value
            except UnexpectedToken:
                return Calculation(CalcType.topCalc, lop)
            try:
                rop = self._read_argument()
            except UnexpectedToken as e:
                raise
            calc = Calculation(CalcType.topCalc, lop, operator, rop)
            lop = calc

    def _read_argument(self):
        try:
            op = self._read_element()
            return op
        except UnexpectedToken as e:
            pass
        try:
            self._require_token(TokenType.lparent)
            op = self._read_calc()
            self._require_token(TokenType.rparent)
            return op
        except UnexpectedToken as e:
            raise

    def _read_test_argument(self):
        try:
            op = None
            self._require_token(TokenType.lparent)
            try:
                op = self._require_token(TokenType.notSign).value
            except UnexpectedToken:
                pass
            lop = self._read_logic_test()
            self._require_token(TokenType.rparent)
            return TestArgument(lop, op)
        except UnexpectedToken as e:
            pass
        try:
            lop = self._read_calc()
            operator = self._require_token(TokenType.testOperator).value
            rop = self._read_calc()
            return TestArgument(lop, operator, rop)
        except UnexpectedToken as e:
            raise

    def _read_top_logic_test(self):
        try:
            lop = self._read_test_argument()
        except UnexpectedToken as e:
            raise
        while True:
            try:
                op = self._require_token(TokenType.topLogicOperator).value
            except UnexpectedToken:
                return LogicTest(TestType.topTest, lop)
            try:
                rop = self._read_test_argument()
            except UnexpectedToken as e:
                raise
            test = LogicTest(TestType.topTest, lop, op, rop)
            lop = test

    def _read_logic_test(self):
        try:
            lop = self._read_top_logic_test()
        except UnexpectedToken as e:
            raise
        while True:
            try:
                op = self._require_token(TokenType.botLogicOperator).value
            except UnexpectedToken:
                return LogicTest(TestType.botTest, lop)
            try:
                rop = self._read_top_logic_test()
            except UnexpectedToken as e:
                raise
            test = LogicTest(TestType.botTest, lop, op, rop)
            lop = test

    def _read_func_expr(self):
        try:
            if self.scanner.peek_token().type != TokenType.mapOperator:
                raise UnexpectedToken("Not a function expression!")
            self.memory.start_new_scope()
            id = self._read_identifier()
            self.memory.register_variable(id)
            self._require_token(TokenType.mapOperator)
            try:
                self.scanner.thread_softly()
                expr = self._read_logic_test()
                self.memory.stop_scope()
                return FunctionExpr(id, expr)
            except UnexpectedToken:
                self.scanner.go_back()
                pass
            expr = self._read_calc()
            self.memory.stop_scope()
            return FunctionExpr(id, expr)
        except UnexpectedToken as e:
            raise

    def _read_sys_func_args(self):
        try:
            self._require_token(TokenType.lparent)
            try:
                args = self._read_func_expr()
            except UnexpectedToken:
                args = None
            self._require_token(TokenType.rparent)
            return args
        except UnexpectedToken as e:
            raise

    def _read_sys_func(self):
        try:
            self.scanner.thread_softly()
            id = self._read_identifier()
            args = self._read_sys_func_args()
        except UnexpectedToken as e:
            raise
        if id.value == 'filter':
            return FilterFunction(args)
        if id.value == 'map':
            return MapFunction(args)
        if id.value == 'length':
            return LengthFunction(args)
        if id.value == 'print':
            return PrintFunction(args)
        self.scanner.go_back()
        raise UnexpectedToken('Not a sys function')

    def _read_cust_func(self):
        pass

    def _read_func_call(self):
        try:
            if self.scanner.peek_token().type != TokenType.dot:
                raise UnexpectedToken("Not a function call!")
        except UnexpectedToken as e:
            raise
        try:
            who = self._read_identifier()
        except UnexpectedToken as e:
            raise
        while (True):
            self._require_token(TokenType.dot)
            try:
                what = self._read_sys_func()
            except UnexpectedToken:
                try:
                    what = self._read_cust_func()
                except UnexpectedToken as e:
                    raise ParseError("Wrong function call!")
            if self._get_token_type() != TokenType.dot:
                return FuncCall(who, what)
            who = FuncCall(who, what)
