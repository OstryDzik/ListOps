from ListOps.src.grammar.numbers import Number


class ForLoop():
    def __init__(self, id, test, list, expr):
        self.id = id
        self.test = test
        self.list = list
        self.expr = expr

    def get_value(self):
        var = None
        self.id.register_variable(None)
        value_list = self.list.get_value().get_value()
        if (isinstance(value_list, Number)):
            value_list = [value_list]
        for i in value_list:
            self.id.update_variable(i)
            if self.test is None or self.test.get_value():
                for j in self.expr:
                    var = j.get_value()
        self.id.delete_value()
        return var