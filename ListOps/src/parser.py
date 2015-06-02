from ListOps.src.grammar.expression import Expression
from ListOps.src.grammar.for_loop import ForLoop
from ListOps.src.grammar.sys_functions import FunctionExpr, FilterFunction, MapFunction, LengthFunction, PrintFunction, \
    FuncCall, \
    SliceFunction
from ListOps.src.grammar.cust_functions import Function, FunctionDefinition
from ListOps.src.grammar.if_statement import IfStatement
from ListOps.src.grammar.logic_test import TestArgument, LogicTest, TestType
from ListOps.src.grammar.numbers import Integer, SignedInteger, Float, SignedFloat, Number
from ListOps.src.grammar.list import List
from ListOps.src.grammar.identifier import Identifier
from ListOps.src.grammar.calculations import CalcType, Calculation
from ListOps.src.grammar.assignment import Assignment, Declaration
from ListOps.src.grammar.program import Program
from ListOps.src.grammar.statement import Statement
from ListOps.src.memory import Memory
from ListOps.src.tokens import TokenType
from ListOps.src.utils import UnexpectedToken, EOFException, ParseException, RunError


class Parser():
    def __init__(self, scanner):
        self.scanner = scanner
        self.memory = Memory()
        self.func_memory = Memory()
        self.notEOF = True

    def parse(self):
        statements = []
        self._advance()
        try:
            while self.notEOF:
                try:
                    statements.append(self._read_cust_function_definition())
                except UnexpectedToken:
                    pass
                statements.append(self._read_statement())
                if self.scanner.get_token().type == TokenType.EOF: break
        except ParseException as e:
            raise
        return Program(statements)

    def parse_and_run(self):
        try:
            program = self.parse()
        except ParseException as e:
            print("Statement error found! :" + str(e) +"\n" + self._get_err_msg())
            return self._get_position()
        try:
            program.run()
            return -1
        except RunError as e:
            print("RunTime error! " + str(e) + " " +"\n"+ self._get_err_msg())
            return self._get_position()


    ## helper methods
    def _advance(self):
        try:
            self.scanner.read_next_token()
        except EOFException:
            print("Encountered end of input")
            self.notEOF = False
            quit()

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
            self._get_err_msg())

    def _get_err_msg(self):
        return "Error: at position {0}, token: {1}, value: {2}".format(self._get_position(),
                                                                     self._get_token_type().value,
                                                                     self._get_token_value())

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

    def _read_function_identifier(self):
        try:
            id = self._require_token(TokenType.id)
        except UnexpectedToken:
            raise
        return Identifier(id.value, self.func_memory)

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
                list.append(num)
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

    def _read_sys_func_call(self):
        try:
            if self.scanner.peek_token().type != TokenType.dot:
                raise UnexpectedToken("Not a system function call!")
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
                raise ParseException("Wrong sys function call!")
            if self._get_token_type() != TokenType.dot:
                return FuncCall(who, what)
            who = FuncCall(who, what)

    def _read_cust_func_header(self):
        try:
            if self.scanner.peek_token().type != TokenType.lparent:
                raise UnexpectedToken("Not a function header!")
        except UnexpectedToken as e:
            raise
        try:
            who = self._read_function_identifier()
        except UnexpectedToken as e:
            raise
        try:
            args = self._read_arguments_list()
        except (ParseException, UnexpectedToken) as e:
            raise
        return (who, args)

    def _read_cust_func_call(self):
        try:
            val = self._read_cust_func_header()
        except (UnexpectedToken, ParseException) as e:
            raise
        return Function(val[0], val[1])

    def _read_return_statement(self):
        try:
            self._require_token(TokenType.keyword, 'return')
        except UnexpectedToken as e:
            raise
        try:
            ret = self._read_element()
            return ret
        except UnexpectedToken:
            return None

    def _read_cust_function_body(self):
        expr = []
        ret = None
        try:
            self._require_token(TokenType.lbrace)
            while (True):
                expr.append(self._read_expression())
                try:
                    ret = self._read_return_statement()
                except UnexpectedToken:
                    pass
                except ParseException as e:
                    raise
                else:
                    break
            try:
                self._require_token(TokenType.rbrace)
            except UnexpectedToken:
                raise ParseException("Wrong function body declaration!")
        except UnexpectedToken as e:
            raise
        return (expr, ret)

    def _read_cust_function_definition(self):
        try:
            self._require_token(TokenType.keyword, 'def')
        except UnexpectedToken as e:
            raise
        try:
            self.memory.start_new_scope()
            head = self._read_cust_func_header()
            body = self._read_cust_function_body()
            self.memory.stop_scope()
            return FunctionDefinition(head[0], head[1], body[0], body[1])
        except (UnexpectedToken, ParseException) as e:
            self.memory.stop_scope()
            raise ParseException("Wrong function definition! " + str(e))


    def _read_slice_call(self):
        try:
            if self.scanner.peek_token().type != TokenType.lsquare:
                raise UnexpectedToken("Not a slice call!")
        except UnexpectedToken as e:
            raise
        try:
            who = self._read_identifier()
        except UnexpectedToken as e:
            raise
        try:
            slice = self._read_slice()
        except UnexpectedToken as e:
            raise
        return FuncCall(who, slice)

    def _read_slice(self):
        self._require_token(TokenType.lsquare)  # safe, read_slice_call ensures that
        try:
            larg = self._read_element()
        except UnexpectedToken:
            larg = None
            pass
        try:
            self._require_token(TokenType.rsquare)
            return SliceFunction(larg, indexOnly=True)
        except:
            pass
        try:
            self._require_token(TokenType.colon)
        except:
            raise ParseException("Wrong range specified!")
        try:
            rarg = self._read_element()
        except UnexpectedToken:
            rarg = None
            pass
        try:
            self._require_token(TokenType.rsquare)
        except UnexpectedToken as e:
            raise
        return SliceFunction(larg, rarg)

    def _read_variable_assignment(self):
        value = None
        try:
            value = self._read_calc()
            return value
        except UnexpectedToken as e:
            pass
        try:
            value = self._read_logic_test()
            return value
        except UnexpectedToken as e:
            pass
        try:
            value = self._read_sys_func_call()
            return value
        except UnexpectedToken as e:
            raise

    def _read_list_assignment(self):
        value = None
        try:
            value = self._read_list_of_numbers()
            return value
        except UnexpectedToken as e:
            pass
        try:
            value = self._read_slice_call()
            return value
        except UnexpectedToken as e:
            pass
        try:
            value = self._read_sys_func_call()
            return value
        except UnexpectedToken as e:
            raise

    def _read_assignment(self):
        try:
            if self.scanner.peek_token().type not in [TokenType.assignOperator, TokenType.lsquare]:
                raise UnexpectedToken("Not an assignment call!")
        except UnexpectedToken as e:
            raise
        try:
            id = self._read_identifier()
            try:
                index = self._read_selection()
            except UnexpectedToken:
                index = None
                pass
            self._require_token(TokenType.assignOperator)
        except UnexpectedToken as e:
            raise
        try:
            value = self._read_cust_func_call()
            return Assignment(id, value, index)
        except UnexpectedToken:
            pass
        try:
            value = self._read_list_assignment()
            return Assignment(id, value, index)
        except UnexpectedToken:
            pass
        try:
            value = self._read_variable_assignment()
            return Assignment(id, value, index)
        except UnexpectedToken as e:
            raise

    def _read_declaration(self):
        try:
            self._require_token(TokenType.keyword, 'var')
        except UnexpectedToken as e:
            raise
        try:
            assgn = self._read_assignment()
            id = assgn.get_id()
            return Declaration(id, assgn)
        except UnexpectedToken as e:
            pass
        try:
            id = self._read_identifier()
            return Declaration(id)
        except UnexpectedToken as e:
            raise ParseException("Wrong variable assignment!")

    def _read_selection(self):
        try:
            self._require_token(TokenType.lsquare)
        except UnexpectedToken as e:
            raise
        try:
            index = self._read_element()
            self._require_token(TokenType.rsquare)
        except UnexpectedToken as e:
            raise ParseException("Wrong selection!")
        return index

    def _read_for_loop(self):
        try:
            self.memory.start_new_scope()
            self._require_token(TokenType.keyword, 'for')
        except UnexpectedToken as e:
            self.memory.stop_scope()
            raise
        try:
            header = self._read_for_loop_header()
            body = self._read_body()
            self.memory.stop_scope()
            return ForLoop(header['id'], header['test'], header['list'], body)
        except UnexpectedToken as e:
            self.memory.stop_scope()
            raise ParseException("Wrong for loop definition! " + str(e))

    def _read_for_loop_header(self):
        try:
            self._require_token(TokenType.lparent)
            id = self._read_identifier()
            self._require_token(TokenType.keyword, 'in')
            list = self._read_identifier()
            try:
                self._require_token(TokenType.colon)
            except UnexpectedToken:
                test = None
            else:
                try:
                    test = self._read_logic_test()
                except UnexpectedToken as e:
                    raise
            self._require_token(TokenType.rparent)
        except UnexpectedToken as e:
            raise
        return {'id': id, 'test': test, 'list': list}

    def _read_body(self):
        expr = []
        try:
            self._require_token(TokenType.lbrace)
            while (True):
                expr.append(self._read_expression())
                try:
                    self._require_token(TokenType.rbrace)
                except UnexpectedToken:
                    pass
                else:
                    break
        except UnexpectedToken as e:
            raise
        return expr

    def _read_if_header(self):
        try:
            self._require_token(TokenType.lparent)
            test = self._read_logic_test()
            self._require_token(TokenType.rparent)
            return test
        except UnexpectedToken as e:
            raise

    def _read_if_statement(self):
        try:
            self._require_token(TokenType.keyword, 'if')
        except UnexpectedToken:
            raise
        try:
            test = self._read_if_header()
            body = self._read_body()
            try:
                self._require_token(TokenType.keyword, 'else')
            except UnexpectedToken:
                return IfStatement(test, body)
            alt_body = self._read_body()
            return IfStatement(test, body, alt_body)
        except UnexpectedToken:
            raise ParseException("Error in If declaration!")

    def _read_expression(self):
        try:
            expr = self._read_declaration()
            return Expression(expr)
        except UnexpectedToken:
            pass
        try:
            expr = self._read_sys_func_call()
            return Expression(expr)
        except UnexpectedToken:
            pass
        try:
            expr = self._read_for_loop()
            return Expression(expr)
        except UnexpectedToken:
            pass
        try:
            expr = self._read_if_statement()
            return Expression(expr)
        except UnexpectedToken:
            pass
        try:
            expr = self._read_assignment()
            return Expression(expr)
        except UnexpectedToken:
            raise ParseException("Invalid expression!")

    def _read_statement(self):
        try:
            stmt = self._read_expression()
            return Statement(stmt)
        except ParseException as e:
            raise
        except UnexpectedToken as e:
            raise
