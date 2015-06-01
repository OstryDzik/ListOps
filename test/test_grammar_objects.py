import unittest

from src.grammar.identifier import Identifier
from src.grammar.list import List
from src.grammar.numbers import Number
from src.grammar.calculations import CalcType, Calculation
from src.parser import Parser
from src.scanner import Scanner


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
