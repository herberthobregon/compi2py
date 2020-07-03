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
    '_BOOL', 'AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST',
    'CONTINUE', 'DEFAULT', 'DO', 'DOUBLE', 'ELSE', 'ENUM', 'EXTERN',
    'FLOAT', 'FOR', 'GOTO', 'IF', 'INLINE', 'INT', 'LONG',
    'REGISTER', 'OFFSETOF',
    'RESTRICT', 'RETURN', 'SHORT', 'SIGNED', 'SIZEOF', 'STATIC', 'STRUCT',
    'SWITCH', 'TYPEDEF', 'UNION', 'UNSIGNED', 'VOID',
    'VOLATILE', 'WHILE'
)

keyword_map = {}

for keyword in keywords:
    if keyword == '_BOOL':
        keyword_map['_Bool'] = keyword
    else:
        keyword_map[keyword.lower()] = keyword

tokens = (
    'RMAIN',
    'RDOUBLE',
    'RMALLOC',
    'RAUTO',
    'RBREAK',
    'RCASE',
    'RCHAR',
    'RCONST',
    'RCONTINUE',
    'RDEFAULT',
    'RDO',
    'RSWITCH',
    'RELSE',
    'RENUM',
    'REXTERN',
    'RFLOAT',
    'RFOR',
    'RIF',
    'INT',
    'RREGISTER',
    'RRETURN',
    'RSIZEOF',
    'RSTRUCT',
    'RVOID',
    'RWHILE',
    'RPRINT',
    'RSCANF',
    'RGOTO',
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
    'RAND',
    'ROR',
    'RNOT',
    'RANDBIT',
    'RORBIT',
    'RNOTBIT',
    'RXORBIT',
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
t_RMAIN = r'main'
t_RDOUBLE = r'double'
t_RMALLOC = r'malloc'
t_RAUTO = r'auto'
t_RBREAK = r'break'
t_RCASE = r'case'
t_RCHAR = r'char'
t_RCONST = r'const'
t_RCONTINUE = r'continue'
t_RDEFAULT = r'default'
t_RFLOAT = r'float'
t_RPRINT = r'printf'
t_RINT = r'int'
t_RSTRUCT = r'struct'
t_RIF = r'if'
t_RELSE = r'else'
t_RWHILE = r'while'
t_RDO = r'do'
t_RFOR = r'for'
t_RSWITCH = r'switch'
t_RSCANF = r'scanf'
t_RGOTO = r'goto'
t_RRETURN = r'return'
t_RVOID = r'void'
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
t_RAND = r'&&'
t_ROR = r'\|\|'
t_RNOT = r'!'
t_RNOTBIT = r'~'
t_TERNARIO = r'\?'
t_RORBIT = r'\|'
t_RANDBIT = r'&'
t_RXORBIT = r'\^'
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
    descripcion = "Caracter no reconocido por MinorC: " + t.value[0]
    ErrorLexico = CError(descripcion, t.lexer.lineno, find_column(entrada, t), "lexico")
    print(ErrorLexico, find_column('', t))
    lErrores.append(ErrorLexico)
    t.lexer.skip(1)
