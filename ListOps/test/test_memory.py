import unittest

from ListOps.src.grammar.numbers import Number
from ListOps.src.grammar.identifier import Identifier
from ListOps.src.memory import Memory
from ListOps.src.utils import UndeclaredVariable


class MemoryTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dict_finds_object(self):
        mem = Memory()
        mem.register_variable(Identifier("a"), Number(-15))
        self.assertEqual(mem.get_variable(Identifier("a")), Number(-15))

    def test_dict_raises_error(self):
        mem = Memory()
        self.assertRaises(UndeclaredVariable, lambda: mem.get_variable(Identifier("a")))

    def test_register_variable(self):
        mem = Memory()
        id = Identifier("a", mem)
        mem.register_variable(id, Number(12))
        self.assertEqual(id.get_value(), Number(12))

    def test_update_nonexistent_variable(self):
        mem = Memory()
        id = Identifier("a", mem)
        self.assertRaises(UndeclaredVariable, lambda: mem.update_variable(id, Number(12)))

    def test_scopes_redeclare_local_variable(self):
        mem = Memory()
        id_global = Identifier("a", mem)
        mem.register_variable(id_global, Number(10))
        mem.start_new_scope()
        id_local = Identifier("a", mem)
        mem.register_variable(id_local, Number(12))
        self.assertEqual(id_local.get_value(), Number(12))
        mem.stop_scope()
        self.assertEqual(id_global.get_value(), Number(10))

    def test_unable_to_redeclare_variable(self):
        mem = Memory()
        id_global = Identifier("a", mem)
        mem.register_variable(id_global, Number(10))
        self.assertRaises(UndeclaredVariable, lambda: mem.register_variable(id_global, Number(12)))

    def test_variable_invisible_from_outside_of_scope(self):
        mem = Memory()
        mem.start_new_scope()
        id = Identifier("a", mem)
        mem.register_variable(id, Number(10))
        mem.stop_scope()
        id = Identifier("a", mem)
        self.assertRaises(UndeclaredVariable, lambda: mem.get_variable(id))

    def test_access_global_variable_from_new_scope(self):
        mem = Memory()
        id = Identifier("a", mem)
        mem.register_variable(id, Number(10))
        mem.start_new_scope()
        id = Identifier("a", mem)
        self.assertEqual(id.get_value(), Number(10))