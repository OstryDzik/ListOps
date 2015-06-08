import unittest

from ListOps.src.grammar.cust_functions import FunctionDefinition, Function
from ListOps.src.grammar.identifier import Identifier
from ListOps.src.grammar.list import List
from ListOps.src.grammar.numbers import Number
from ListOps.src.grammar.calculations import CalcType, Calculation
from ListOps.src.parser import Parser
from ListOps.src.scanner import Scanner


class ObjectsTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_calc(self):
        calc = Calculation(CalcType.topCalc, Number(12), '*', Number(3))
        self.assertEqual(calc.get_value(), Number(36))


class FunctionTests(unittest.TestCase):
    def setUp(self):
        self.list = List([Number(1), Number(2), Number(3), Number(4), Number(5)])

    def tearDown(self):
        pass

    def test_list_filter(self):
        input = "filter(a->a<=2)"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        expr = parser._read_sys_func()
        result = self.list.call_function(expr)
        self.assertEqual(result, List([Number(1), Number(2)]))

    def test_list_map(self):
        input = "map(a->a+2)"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        expr = parser._read_sys_func()
        result = self.list.call_function(expr)
        self.assertEqual(result, List([Number(3), Number(4), Number(5), Number(6), Number(7)]))

    def test_list_length(self):
        input = "length()"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        expr = parser._read_sys_func()
        result = self.list.call_function(expr)
        self.assertEqual(self.list.length(), Number(5))

    def test_for_loop(self):
        value = "for (a in b : a<2){c[a]=a+1}"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        parser.memory.register_variable(Identifier('b'), List([Number(0), Number(1)]))
        parser.memory.register_variable(Identifier('c'), List([Number(5), Number(6)]))
        loop = parser._read_for_loop()
        outcome = loop.get_value()
        self.assertEqual(parser.memory.get_variable(Identifier('c')), List([Number(1), Number(2)]))

    def test_if_else_statement(self):
        value = "if(a>5){a=8}else{a=12}"
        scanner = Scanner(value)
        parser = Parser(scanner)
        parser._advance()
        parser.memory.register_variable(Identifier('a'), Number((4)))
        loop = parser._read_if_statement()
        outcome = loop.get_value()
        self.assertEqual(parser.memory.get_variable(Identifier('a')), Number(12))

    def test_execute_slice_call(self):
        input = "a[1:3]"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser.memory.register_variable(Identifier("a"), List([Number(1), Number(2), Number(3), Number(4), Number(5)]))
        parser._advance()
        slice = parser._read_slice_call()
        self.assertEqual(slice.get_value(), List([Number(2), Number(3)]))
        input = "a[1:b]"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser.memory.register_variable(Identifier("a"), List([Number(1), Number(2), Number(3), Number(4), Number(5)]))
        parser.memory.register_variable(Identifier("b"), Number(3))
        parser._advance()
        slice = parser._read_slice_call()
        self.assertEqual(slice.get_value(), List([Number(2), Number(3)]))

    def test_define_and_call_function(self):
        input = """
        def x(a,b,c)
        {
            var d = a + b + c
            return
        }
        x(1,2,3)"""
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        func = parser._read_cust_function_definition()
        func_call = parser._read_cust_func_call()
        self.assertEqual(isinstance(func, FunctionDefinition), True)
        self.assertEqual(isinstance(func_call, Function), True)
        func.get_value()
        func_call.get_value()