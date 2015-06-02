import sys
if "E:\Studia2015\TKOM" not in sys.path:
    sys.path.append("E:\Studia2015\TKOM")

from ListOps.src.parser import Parser
from ListOps.src.scanner import Scanner
from ListOps.src.utils import HELP_MSG


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
def main():
    if len(sys.argv) < 2:
        sys.exit(HELP_MSG)
    try:
        with open(sys.argv[1], "r") as myfile:
            code = myfile.read()
    except:
        sys.exit("ERROR. The file doesn't exist!")


    print("Parsing source:")
    print(code)
    print("Output:")
    parser = Parser(Scanner(code))
    result = parser.parse_and_run()
    if result > 0:
        print("")
        print_line(code, result)

if __name__ == "__main__":
    main()


