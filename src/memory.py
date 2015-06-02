from src.grammar.cust_functions import FunctionDefinition
from src.grammar.list import List
from src.grammar.numbers import Literal
from src.utils import UndeclaredVariable


class Memory():

    def __init__(self):
        self.scopes = [{}]
        self.currScope = 0
        self.store_scope = 0

    def register_variable(self, id, value=None):
        if self._check_variable(id):
            raise UndeclaredVariable("Variable already exists: " + id.value)
        self.scopes[id.get_scope()][id.value] = value

    def update_variable(self, id, value):
        if self._check_variable(id):
            self.scopes[id.get_scope()][id.value] = value
            return
        if self._check_global_variable(id):
            self.scopes[0][id.value] = value
            return
        raise UndeclaredVariable("Tried to use undeclared variable: {0}".format(id.value))

    def get_variable(self, id):
        if self._check_variable(id):
            var = self.scopes[id.get_scope()][id.value]
        elif self._check_global_variable(id):
            var = self.scopes[0][id.value]
        else:
            raise UndeclaredVariable("Tried to use undeclared variable: {0}".format(id.value))
        if not isinstance(var, Literal) and not isinstance(var, List) and not isinstance(var, FunctionDefinition):
            return var.get_value()
        else:
            return var

    def _check_variable(self, id):
        return id.value in self.scopes[id.get_scope()]

    def _check_global_variable(self, id):
        return id.value in self.scopes[0]

    def get_scope(self):
        return self.currScope

    def start_new_scope(self):
        self.store_scope = self.currScope
        self.scopes.append({})
        self.currScope = len(self.scopes) - 1
        return self.currScope

    def stop_scope(self):
        self.currScope = self.store_scope

    def delete_variable(self, id):
        if self._check_variable(id):
            del (self.scopes[id.get_scope()][id.value])