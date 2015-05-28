import unittest

from src.grammar.numbers import Number
from src.grammar.objects import Calculation, CalcType


class ObjectsTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_calc(self):
        calc = Calculation(CalcType.topCalc, Number(12, 1), '*', Number(3, 1))
        self.assertEqual(calc.get_value(), 36)