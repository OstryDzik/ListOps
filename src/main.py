import sys

from src.parser import Parser
from src.scanner import Scanner
from src.utils import HELP_MSG


__author__ = 'Filip'


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def print_line(str, index):
    indexes = find(str, '\n')
    spaces = ""
    prev = 0
    curr = 0
    for i in indexes:
        prev = curr
        curr = i
        if curr >= index:
            break
    for i in range(0, (index - prev - 1)):
        spaces += ' '
    spaces += '^'
    print(str[prev + 1: curr])
    print(spaces)


####Main####

if len(sys.argv) < 1:
    sys.exit(HELP_MSG)
try:
    with open("data.txt", "r") as myfile:
        code = data = myfile.read()
except:
    sys.exit("ERROR. The file doesn't exist!")
parser = Parser(Scanner(code))
result = parser.parse_and_run()
if result > 0:
    print_line(code, result)



