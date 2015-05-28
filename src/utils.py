EOF = "$"


class ParseException(Exception):
    pass


class TokenMismatchException(Exception):
    pass


class UnexpectedToken(Exception):
    pass


class ScannerException(Exception):
    pass


class EOFException(Exception):
    pass


class UndeclaredVariable(Exception):
    pass


KEYWORDS = ['def', 'for', 'in', 'if', 'else', 'var', 'list']
TOP_OPERATORS = ['*', '/', '%']
BOT_OPERATORS = ['+', '-']

