import inspect

from src.utils import TokenMismatchException, EOF, KEYWORDS, TOP_OPERATORS, BOT_OPERATORS, ScannerException, \
    EOFException
from src.tokens import TokenType, Token


class Scanner():
    token = None
    position = 0
    stored_position = 0
    stored = False

    def __init__(self, s):
        self.input = s
        self.input += EOF

    def get_token(self):
        if self.token is None:
            self.token = Token(TokenType.EOF, EOF)
        return self.token

    def read_next_token(self):
        if self.position != 0 and self.token.type == TokenType.EOF:
            raise EOFException("End of input!")
        member_list = inspect.getmembers(self, predicate=inspect.ismethod)
        self._skip_white_space()
        for (member_name, member_value) in member_list:
            if member_name.startswith("_try"):
                try:
                    member_value()
                except TokenMismatchException:
                    pass
                else:
                    return self.token
        raise ScannerException("Scanner error, no token read!")

    def peek_token(self):
        pos = self.position
        token = self.token
        try:
            next_token = self.read_next_token()
        except ScannerException as e:
            return Token(TokenType.EOF, EOF)
        self.position = pos
        self.token = token
        return next_token

    def get_position(self):
        return self.position

    def thread_softly(self):
        self.snapshot_pos = self.position
        self.snapshot_token = self.token

    def go_back(self):
        if self.snapshot_token is not None:
            self.token = self.snapshot_token
            self.position = self.snapshot_pos
            self.snapshot_pos = None
            self.snapshot_token = None
    ## string control methods

    def _store_position(self):
        self.stored_position = self.position
        self.stored = True

    def _rewind(self):
        if self.stored == True:
            self.position = self.stored_position
            self.stored = False
        else:
            raise ScannerException("Rewinding without stored position!")

    def _skip_white_space(self):
        while self.input[self.position].isspace():
            self.position += 1

    def _peek_char(self):
        return self.input[self.position]

    def _pop_char(self):
        self.position += 1
        return self.input[self.position - 1]

    ## token scanning methods

    def _try_number(self):
        try:
            self._store_position()
            integer_value = self._read_integer()
        except TokenMismatchException as e:
            self._rewind()
            raise
        try:
            self._store_position()
            float_value = self._read_float_value()
        except TokenMismatchException as e:
            self._rewind()
            self.token = Token(TokenType.integer, integer_value)
        else:
            self.token = Token(TokenType.float, integer_value + float_value)

    def _try_lparent(self):
        try:
            val = self._read_one_char('(')
        except TokenMismatchException as e:
            raise
        else:
            self.token = Token(TokenType.lparent, val)

    def _try_rparent(self):
        try:
            val = self._read_one_char(')')
        except TokenMismatchException as e:
            raise
        else:
            self.token = Token(TokenType.rparent, val)

    def _try_lbrace(self):
        try:
            val = self._read_one_char('{')
        except TokenMismatchException as e:
            raise
        else:
            self.token = Token(TokenType.lbrace, val)

    def _try_rbrace(self):
        try:
            val = self._read_one_char('}')
        except TokenMismatchException as e:
            raise
        else:
            self.token = Token(TokenType.rbrace, val)

    def _try_lsquare(self):
        try:
            val = self._read_one_char('[')
        except TokenMismatchException as e:
            raise
        else:
            self.token = Token(TokenType.lsquare, val)

    def _try_rsquare(self):
        try:
            val = self._read_one_char(']')
        except TokenMismatchException as e:
            raise
        else:
            self.token = Token(TokenType.rsquare, val)

    def _try_dot(self):
        try:
            self._store_position()
            val = self._read_one_char('.')
            if self._peek_char().isdigit():
                self._rewind()
                raise TokenMismatchException("Not a proper dot!")
        except TokenMismatchException as e:
            raise
        else:
            self.token = Token(TokenType.dot, val)

    def _try_comma(self):
        try:
            val = self._read_one_char(',')
        except TokenMismatchException as e:
            raise
        else:
            self.token = Token(TokenType.comma, val)

    def _try_not_sign(self):
        try:
            val = self._read_one_char('!')
        except TokenMismatchException as e:
            raise
        else:
            self.token = Token(TokenType.notSign, val)

    def _try_assign_operator(self):
        try:
            self._store_position()
            val = self._read_one_char('=')
            if self._peek_char() == '=':
                self._rewind()
                raise TokenMismatchException("It's a logical operator")
        except TokenMismatchException as e:
            raise
        else:
            self.token = Token(TokenType.assignOperator, val)

    def _try_range_operator(self):
        try:
            val = self._read_one_char(':')
        except TokenMismatchException as e:
            raise
        else:
            self.token = Token(TokenType.rangeOperator, val)

    def _try_map_operator(self):
        try:
            self._store_position()
            val = self._read_one_char('-')
            val += self._read_one_char('>')
        except TokenMismatchException as e:
            self._rewind()
            raise
        else:
            self.token = Token(TokenType.mapOperator, val)

    def _try_top_logic_operator(self):
        try:
            self._store_position()
            val = self._read_one_char('|')
            val += self._read_one_char('|')
        except TokenMismatchException as e:
            self._rewind()
            raise
        else:
            self.token = Token(TokenType.topLogicOperator, val)

    def _try_bot_logic_operator(self):
        try:
            self._store_position()
            val = self._read_one_char('&')
            val += self._read_one_char('&')
        except TokenMismatchException as e:
            self._rewind()
            raise
        else:
            self.token = Token(TokenType.botLogicOperator, val)

    def _try_string(self):
        try:
            val = self._read_alfa_string()
        except TokenMismatchException as e:
            raise
        try:
            self._read_keyword(val)
        except TokenMismatchException as e:
            self.token = Token(TokenType.id, val)
        else:
            self.token = Token(TokenType.keyword, val)

    def _try_top_operator(self):
        val = ""
        for char in TOP_OPERATORS:
            try:
                val = self._read_one_char(char)
            except TokenMismatchException as e:
                pass
            else:
                self.token = Token(TokenType.topOperator, char)
                return
        raise TokenMismatchException("Not a top operator")

    def _try_bot_operator(self):
        val = ""
        self._store_position()
        for char in BOT_OPERATORS:
            try:
                val = self._read_one_char(char)
                if val == "-" and self._peek_char() == ">":
                    self._rewind()
                    raise TokenMismatchException("Not a bot operator")
            except TokenMismatchException as e:
                pass
            else:
                self.token = Token(TokenType.botOperator, char)
                return
        raise TokenMismatchException("Not a bot operator")

    def _try_test_operator(self):
        val = ""
        self._store_position()
        for char in ["<", ">", "=", "!"]:
            try:
                val = self._read_one_char(char)
            except TokenMismatchException as e:
                pass
            else:
                break
        try:
            val += self._read_one_char("=")
        except TokenMismatchException as e:
            if (val == "<" or val == ">"):
                self.token = Token(TokenType.testOperator, val)
                return
            self._rewind()
            raise TokenMismatchException("Not a test operator")
        else:
            self.token = Token(TokenType.testOperator, val)

    def _try_EOF(self):
        val = ""
        try:
            val = self._read_one_char(EOF)
        except TokenMismatchException as e:
            raise
        self.token = Token(TokenType.EOF, val)

    ## helper methods

    def _read_keyword(self, val):
        if val in KEYWORDS:
            return val
        raise TokenMismatchException("Not a keyword")

    def _read_one_char(self, char):
        val = ""
        if self._peek_char() == char:
            val = self._pop_char()
        else:
            raise TokenMismatchException("Wrong char, wanted {0}, got {1}".format(char, self._peek_char()))
        return val

    def _read_integer(self):
        val = ""
        # non zero on start
        if self._peek_char().isdigit() and self._peek_char() != '0':
            val += self._pop_char()
        else:
            raise TokenMismatchException("Literal must start with non-0 digit!")
        # get digits
        while self._peek_char().isdigit():
            val += self._pop_char()
        return val

    def _read_float_value(self):
        val = ""
        if self._peek_char() == '.':
            val += self._pop_char()
        else:
            raise TokenMismatchException("Float part must start with . !")
        while self._peek_char().isdigit():
            val += self._pop_char()
        if val == '.':
            raise TokenMismatchException("Read no digits after")
        return val

    def _read_alfa_string(self):
        val = ""
        if not self._peek_char().isalpha():
            raise TokenMismatchException("Token must start with letter")
        while self._peek_char().isdigit() or self._peek_char().isalpha() or self._peek_char() == '_':
            val += self._pop_char()
        return val