class IfStatement():
    def __init__(self, test, expr, alt_expr=None):
        self.test = test
        self.expr = expr
        self.alt_expr = alt_expr

    def get_value(self):
        var = None
        if self.test.get_value():
            for i in self.expr:
                var = i.get_value()
            return var
        elif self.alt_expr is not None:
            for i in self.alt_expr:
                var = i.get_value()
            return var