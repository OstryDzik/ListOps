from src.utils import ScannerException, EOFException

__author__ = 'Filip'

from src import scanner

s = """123
"""

p = scanner.Scanner(s)
while (True):
    try:
        p.read_next_token()
        t = p.get_token()
        t.print()
    except ScannerException as e:
        print(e)
        break
    except EOFException as e:
        print(e)
        break
