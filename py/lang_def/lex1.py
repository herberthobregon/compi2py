from ply import lex
digit            = r'([0-9])'
nondigit         = r'([_A-Za-z])'
identifier       = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'  

reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE'
}

tokens = (
    "PLUS",
    "MINUS",
    "TIMES",
    "DIV",
    "LPAREN",
    "RPAREN",
    "NUMBER",
)

t_ignore = " \t"
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIV = r"/"
t_LPAREN = r"\("
t_RPAREN = r"\)"

@lex.TOKEN(identifier)
def t_ID(t):
    return t

def t_NUMBER(t):
    r"[0-9]+"
    t.value = int(t.value)
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Invalid Token:", t.value[0])
    t.lexer.skip(1)
