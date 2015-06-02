EOF = "$"


class RunError(Exception):
    pass

class UnsupportedOperation(Exception):
    pass

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


KEYWORDS = ['def', 'for', 'in', 'if', 'else', 'var', 'list', 'return']
TOP_OPERATORS = ['*', '/', '%']
BOT_OPERATORS = ['+', '-']

HELP_MSG = """
Please provide a file name with code to compile!
"""
