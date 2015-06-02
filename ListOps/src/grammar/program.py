class Program():
    def __init__(self, statements):
        self.statements = statements

    def run(self):
        for i in self.statements:
            i.get_value()