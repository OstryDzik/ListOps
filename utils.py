EOF = "$"


class ParseException(Exception):
    pass


KEYWORDS = ['def', 'for', 'in', 'if', 'else', 'var', 'list']
OPERATOR_CHARS = ['*', '/', '%', '+', '-','=','>','<','!','.','&','|',',',':']
OPERATORS=['*','/','%','+','-','=','==','>=','<=','!','!=','&&','||','->',',','.','<','>']

