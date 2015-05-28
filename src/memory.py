from src.utils import UndeclaredVariable


class Memory():
    dict = {}

    def __init__(self):
        self.dict = {}

    def register_variable(self, id, value):
        self.dict[id.value] = value

    def update_variable(self, id, value):
        if self.check_variable(id):
            self.register_variable(id, value)
            return
        raise UndeclaredVariable("Tried to use undeclared variable: {0}".format(id.value))

    def get_variable(self, id):
        if self.check_variable(id):
            return self.dict[id.value]
        raise UndeclaredVariable("Tried to use undeclared variable: {0}".format(id.value))

    def get_variable_value(self, id):
        try:
            return self.get_variable(id).get_value()
        except UndeclaredVariable as e:
            raise

    def check_variable(self, id):
        return id.value in self.dict


