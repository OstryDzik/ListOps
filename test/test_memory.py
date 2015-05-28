import unittest
from src.grammar.numbers import Number
from src.grammar.objects import Identifier
from src.memory import Memory
from src.utils import UndeclaredVariable


class MemoryTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dict_finds_object(self):
        mem = Memory()
        mem.register_variable(Identifier("a"), Number(-15, 1))
        self.assertEqual(mem.get_variable(Identifier("a")), Number(-15, 1))

    def test_dict_raises_error(self):
        mem = Memory()
        self.assertRaises(UndeclaredVariable, lambda: mem.get_variable(Identifier("a")))

    def test_register_variable(self):
        mem = Memory()
        id = Identifier("a", mem)
        mem.register_variable(id, Number(12, 1))
        self.assertEqual(id.get_value(), 12)

    def test_update_nonexistent_variable(self):
        mem = Memory()
        id = Identifier("a", mem)
        self.assertRaises(UndeclaredVariable, lambda: mem.update_variable(id, Number(12, 1)))