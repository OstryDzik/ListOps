import tokens
import utils

class ScannerException(Exception):
    pass

class Scanner():
    def __init__(self, s):
        self.position = 0
        self.input = s
        self.input += utils.EOF
        self.tokens = []

    def skipWhiteSpace(self):
        while self.input[self.position].isspace():
            self.position += 1

    def peekChar(self):
        return self.input[self.position]

    def parseInput(self):
        while self.input[self.position] != utils.EOF:
            self.skipWhiteSpace()
            if self.peekChar().isdigit():
                self.tokens.append(self.parseNumToken())
            elif self.peekChar().isalpha():
                self.tokens.append(self.parseAlfaToken())
            elif self.peekChar() in utils.OPERATOR_CHARS:
                self.tokens.append(self.parseOperator())
            elif self.peekChar() in [')',']','[','(']:
                self.tokens.append(tokens.Parenthesis(self.popChar()))
            elif self.peekChar() in ['{','}']:
                self.tokens.append(tokens.Braces(self.popChar()))
            elif self.peekChar() == utils.EOF:
                break
            else:
                raise ScannerException("Wrong char! "+ self.peekChar())
        return self.tokens

    def popChar(self):
        self.position+=1
        return self.input[self.position-1]

    def parseNumToken(self):
        val = ""
        while self.peekChar().isdigit():
            val += self.popChar()
        return tokens.NumString(val)

    def parseAlfaToken(self):
        val = ""
        while self.peekChar().isalpha() or self.peekChar()=='_' or self.peekChar().isdigit():
            val += self.popChar()
        if val in utils.KEYWORDS:
            return tokens.Keyword(val)
        else:
            return tokens.AlphaString(val)

    def parseOperator(self):
        val = ""
        while self.peekChar() in utils.OPERATOR_CHARS:
            val+= self.popChar()
        if val in utils.OPERATORS:
            return tokens.Operator(val)
        else:
            raise ScannerException(val)