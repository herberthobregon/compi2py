from .globales2 import *
from ply.lex import TOKEN

D = r'[0-9]'
L = r'[a-zA-Z_]'
H = r'[a-fA-F0-9]'
E = r'[Ee][+-]?{D}+'
FS = r'(f|F|l|L)'
IS = r'(u|U|l|L)*'
#
# Reserved keywords
#
keywords = (
    'AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST',
    'CONTINUE', 'DEFAULT', 'DO', 'DOUBLE', 'ELSE', 'ENUM', 'EXTERN',
    'FLOAT', 'FOR', 'GOTO', 'IF', 'INLINE', 'INT', 'LONG',
    'REGISTER', 'OFFSETOF',
    'RESTRICT', 'RETURN', 'SHORT', 'SIGNED', 'SIZEOF', 'STATIC', 'STRUCT',
    'SWITCH', 'TYPEDEF', 'UNION', 'UNSIGNED', 'VOID',
    'VOLATILE', 'WHILE'
)

keyword_map = {}

for keyword in keywords:
    keyword_map[keyword.lower()] = keyword

tokens = (
    'MAIN',
    'DOUBLE',
    'MALLOC',
    'AUTO',
    'BREAK',
    'CASE',
    'CHAR',
    'CONST',
    'CONTINUE',
    'DEFAULT',
    'DO',
    'SWITCH',
    'ELSE',
    'ENUM',
    'EXTERN',
    'FLOAT',
    'FOR',
    'IF',
    'INT',
    'REGISTER',
    'RETURN',
    'SIZEOF',
    'STRUCT',
    'VOID',
    'WHILE',
    'PRINT',
    'SCANF',
    'GOTO',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'LLAVEIZQ',
    'LLAVEDER',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MODULO',
    'PUNTO',
    'COMA',
    'DOBLEACCESOPUNTERO',
    'AND',
    'OR',
    'NOT',
    'ANDBIT',
    'ORBIT',
    'NOTBIT',
    'XORBIT',
    'SHIFTIZQ',
    'SHIFTDER',
    'IGUAL',
    'DIFERENTE',
    'MAYORIGUAL',
    'MENORIGUAL',
    'AUMENTO',
    'DECREMENTO',
    'MAYOR',
    'MENOR',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'PTCOMA',
    'DOSPUNTOS',
    'ID',
    'ASIG',
    'ASIGMAS',
    'ASIGMENOS',
    'ASIGPOR',
    'ASIGDIV',
    'ASIGMODULO',
    'ASIGSHIFTIZQ',
    'ASIGSHITFDER',
    'ASIGAND',
    'ASIGOR',
    'ASIGXOR',
    'TERNARIO'
)

# Tokens
t_MAIN = r'main'
t_DOUBLE = r'double'
t_MALLOC = r'malloc'
t_AUTO = r'auto'
t_BREAK = r'break'
t_CASE = r'case'
t_CHAR = r'char'
t_CONST = r'const'
t_CONTINUE = r'continue'
t_DEFAULT = r'default'
t_FLOAT = r'float'
t_PRINT = r'printf'
t_INT = r'int'
t_STRUCT = r'struct'
t_IF = r'if'
t_ELSE = r'else'
t_WHILE = r'while'
t_DO = r'do'
t_FOR = r'for'
t_SWITCH = r'switch'
t_SCANF = r'scanf'
t_GOTO = r'goto'
t_RETURN = r'return'
t_VOID = r'void'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_MODULO = r'%'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_NOTBIT = r'~'
t_TERNARIO = r'\?'
t_ORBIT = r'\|'
t_ANDBIT = r'&'
t_XORBIT = r'\^'
t_SHIFTIZQ = r'<<'
t_SHIFTDER = r'>>'
t_IGUAL = r'=='
t_DIFERENTE = r'!='
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_AUMENTO = r'\+\+'
t_DECREMENTO = r'--'
t_MAYOR = r'>'
t_MENOR = r'<'
t_PTCOMA = r';'
t_COMA = r','
t_PUNTO = r'\.'
t_DOSPUNTOS = r':'
t_ASIG = r'\='
t_ASIGMAS = r'\+\='
t_ASIGMENOS = r'\-\='
t_ASIGPOR = r'\*\='
t_ASIGDIV = r'\/\='
t_ASIGMODULO = r'\%\='
t_ASIGSHIFTIZQ = r'\<\<\='
t_ASIGSHITFDER = r'\>\>\='
t_ASIGAND = r'\&\='
t_ASIGOR = r'\|\='
t_ASIGXOR = r'\^\='
t_ignore = " \t"

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keyword_map.get(t.value, "ID")
    return t


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Floaat value too large %d", t.value)
        t.value = 0
    return t


def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_CADENA(t):
    r'(\'|\").*?(\"|\')'
    t.value = t.value[1:-1]  # remuevo las comillas
    return t


def t_COMMENT(t):
    r"//.*\n"
    t.lexer.lineno += 1


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def find_column(input, token):
    line_start = input.rfind(input, 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_error(t):
    descripcion = "Caracter no reconocido por MinorC: " + t.value
    ErrorLexico = CError(descripcion, t.lexer.lineno, find_column(entrada, t), "lexico")
    print("ErrorLexico", ErrorLexico)
    lErrores.append(ErrorLexico)
    t.lexer.skip(1)
