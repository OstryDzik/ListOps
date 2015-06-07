from ListOps.src.grammar.cust_functions import FunctionDefinition
from ListOps.src.grammar.list import List
from ListOps.src.grammar.numbers import Literal
from ListOps.src.utils import UndeclaredVariable


class Memory():

    def __init__(self):
        self.scopes = [{}]
        self.currScope = [0]
        self.store_scope = 0

    def register_variable(self, id, value=None):
        if self._check_variable(id):
            raise UndeclaredVariable("Variable already exists: " + id.value)
        self.scopes[id.get_scope()[-1]][id.value] = value

    def update_variable(self, id, value):
        if self._check_variable(id):
            self.scopes[id.get_scope()[-1]][id.value] = value
            return
        if self._check_global_variable(id)[0]:
            self.scopes[self._check_global_variable(id)[1]][id.value] = value
            return
        raise UndeclaredVariable("Tried to use undeclared variable: {0}".format(id.value))

    def get_variable(self, id):
        if self._check_variable(id):
            var = self.scopes[id.get_scope()[-1]][id.value]
        elif self._check_global_variable(id)[0]:
            var = self.scopes[self._check_global_variable(id)[1]][id.value]
        else:
            raise UndeclaredVariable("Tried to use undeclared variable: {0}".format(id.value))
        if not isinstance(var, Literal) and not isinstance(var, List) and not isinstance(var, FunctionDefinition) and var is not None:
            return var.get_value()
        else:
            return var

    def _check_variable(self, id):
        return id.value in self.scopes[id.get_scope()[-1]]

    def _check_global_variable(self, id):
        for i in id.get_scope():
            if id.value in self.scopes[i]:
                return (True,i)
        return (False,-1)

    def get_scope(self):
        return self.currScope.copy()

    def start_new_scope(self):
        self.scopes.append({})
        curScope = len(self.scopes) - 1
        self.currScope.append(curScope)
        return self.currScope.copy()

    def stop_scope(self):
        self.currScope.pop()

    def delete_variable(self, id):
        if self._check_variable(id):
            del (self.scopes[id.get_scope()[-1]][id.value])