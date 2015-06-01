import unittest

from src.grammar.list import List
from src.grammar.numbers import Number, Integer
from src.grammar.calculations import CalcType, Calculation
from src.parser import Parser
from src.scanner import Scanner


class ObjectsTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_calc(self):
        calc = Calculation(CalcType.topCalc, Number(12, 1), '*', Number(3, 1))
        self.assertEqual(calc.get_value(), 36)


class FunctionTests(unittest.TestCase):
    def setUp(self):
        self.list = List([1, 2, 3, 4, 5])

    def tearDown(self):
        pass

    def test_list_filter(self):
        input = "filter(a->a<=2)"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        expr = parser._read_sys_func()
        result = self.list.call_function(expr)
        self.assertEqual(result, List([1, 2]))

    def test_list_map(self):
        input = "map(a->a+2)"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        expr = parser._read_sys_func()
        result = self.list.call_function(expr)
        self.assertEqual(result, List([3, 4, 5, 6, 7]))

    def test_list_length(self):
        input = "length()"
        scanner = Scanner(input)
        parser = Parser(scanner)
        parser._advance()
        expr = parser._read_sys_func()
        result = self.list.call_function(expr)
        self.assertEqual(self.list.length(), Integer(5))
