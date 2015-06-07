class Identifier():
    value = ""

    def __init__(self, value, memory=None):
        self.value = value
        self.memory = memory
        if memory is None:
            self.scope = [0]
        else:
            self.scope = memory.get_scope()


    def __eq__(self, other):
        return self.value == other.value and self.scope == self.scope

    def __ne__(self, other):
        return self.value != other.value or self.scope != self.scope

    def get_value(self):
        return self.memory.get_variable(self)

    def update_variable(self, value):
        self.memory.update_variable(self, value)

    def register_variable(self, value):
        self.memory.register_variable(self, value)

    def get_name(self):
        return self.value

    def get_scope(self):
        return self.scope

    def delete_value(self):
        self.memory.delete_variable(self)