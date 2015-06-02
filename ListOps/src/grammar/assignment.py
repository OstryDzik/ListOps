from ListOps.src.grammar.list import List


class Assignment():
    def __init__(self, id, value, index=None):
        self.id = id
        self.value = value
        self.index = index

    def get_value(self):
        if self.index is None:
            if isinstance(self.value, List):
                self.id.update_variable(self.value)
            else:
                self.id.update_variable(self.value.get_value())
        else:
            list = self.id.get_value()
            number_list = list.get_value()
            index = self.index.get_value()
            number_list[index] = self.value.get_value()
            self.id.update_variable(list)

    def get_id(self):
        return self.id


class Declaration():
    def __init__(self, id, assignment=None):
        self.id = id
        self.assignment = assignment

    def get_value(self):
        self.id.register_variable(None)
        if self.assignment is not None:
            self.assignment.get_value()