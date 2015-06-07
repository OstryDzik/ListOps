from io import StringIO
import unittest
import sys

from ListOps.src.parser import Parser
from ListOps.src.scanner import Scanner


class ProgramTest(unittest.TestCase):
    def setUp(self):
        self.saved_stdout = sys.stdout
        self.out = StringIO()
        sys.stdout = self.out
        #
        # output = out.getvalue().strip()
        # assert output == 'hello world!'


    def tearDown(self):
        sys.stdout = self.saved_stdout

    def test_parse_combined_statements(self):
        value = """
        var a = {1,2,3,4}
        a.print()
        a=a.map(b->b*2)
        a.print()
        for (r in a : r>4){r.print()}
        var b = a.filter(b->b>6)
        var d = b.length()
        if (d <= 1)
        {
            b.print()
            a.print()
        }
        else
        {
            d.print()
        }
        """
        scanner = Scanner(value)
        parser = Parser(scanner)
        program = parser.parse()
        self.assertEqual(len(program.statements), 8)
        program.run()
        output = self.out.getvalue().strip()
        assert output == '[1, 2, 3, 4]\n[2, 4, 6, 8]\n6\n8\n[8]\n[2, 4, 6, 8]'

    def test_parse_combined_more_statements(self):
        value = """
        var a = {1,2,3,4}
        a=a.map(b->b*2).print()
        var b = a[1:8]
        b.print()
        def x(y)
        {
            y = y*2
            return y
        }
        a = x(5)
        a.print()
        """
        scanner = Scanner(value)
        parser = Parser(scanner)
        program = parser.parse()
        program.run()
        output = self.out.getvalue().strip()
        assert output == '[2, 4, 6, 8]\n[4, 6, 8]\n10'

    def test_types(self):
        value = """
        var b = 5
        var e = b.filter(b->b>4)
        var c = b.map(a->a+5)
        var d = b.length()
        c.print()
        d.print()
        e.print()
        """
        scanner = Scanner(value)
        parser = Parser(scanner)
        program = parser.parse()
        program.run()
        output = self.out.getvalue().strip()
        assert output == '10\n1\n5'

    def test_func(self):
        value = """
        var a = {1,2,3,4}
        def medium(a)
        {
            var sum = 0
            for (x in a)
            {
                sum = sum + x
            }
            var len
            len = a.length()
            sum = sum / len
            return sum
        }
        var med = medium(a)
        med.print()
        """
        scanner = Scanner(value)
        parser = Parser(scanner)
        program = parser.parse()
        program.run()
        output = self.out.getvalue().strip()
        assert output == '2.5'