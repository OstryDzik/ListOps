from src.utils import UndeclaredVariable


class Memory():

    def __init__(self):
        self.scopes = [{}]
        self.currScope = 0

    def register_variable(self, id, value=None):
        if self.check_variable(id):
            raise UndeclaredVariable("Variable already exists!")
        self.scopes[self.currScope][id.value] = value

    def update_variable(self, id, value):
        if self.check_variable(id):
            self.scopes[id.get_scope()][id.value] = value
            return
        if self.check_global_variable(id):
            self.scopes[0][id.value] = value
            return
        raise UndeclaredVariable("Tried to use undeclared variable: {0}".format(id.value))

    def get_variable(self, id):
        if self.check_variable(id):
            return self.scopes[id.get_scope()][id.value]
        if self.check_global_variable(id):
            return self.scopes[0][id.value]
        raise UndeclaredVariable("Tried to use undeclared variable: {0}".format(id.value))

    def get_variable_value(self, id):
        try:
            return self.get_variable(id)
        except UndeclaredVariable as e:
            raise

    def check_variable(self, id):
        return id.value in self.scopes[id.get_scope()]

    def check_global_variable(self, id):
        return id.value in self.scopes[0]

    def get_scope(self):
        return self.currScope

    def start_new_scope(self):
        self.scopes.append({})
        self.currScope = len(self.scopes) - 1
        return self.currScope

    def stop_scope(self):
        self.currScope = 0