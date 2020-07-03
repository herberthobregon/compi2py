from compi.gramaticas.globales import *

tokens = (
    "RABS",
    "RMAIN",
    "RGOTO",
    "RREAD",
    "REXIT",
    "RPRINT",
    "RUNSET",
    "RINT",
    "RFLOAT",
    "RCHAR",
    "RARRAY",
    "RXOR",
    "RIF",
    "PARIZQ",
    "PARDER",
    "CORIZQ",
    "CORDER",
    "MAS",
    "MENOS",
    "POR",
    "DIVIDIDO",
    "MODULO",
    "RAND",
    "ROR",
    "RNOT",
    "RANDBIT",
    "RORBIT",
    "RNOTBIT",
    "RXORBIT",
    "SHIFTIZQ",
    "SHIFTDER",
    "IGUAL",
    "DIFERENTE",
    "MAYORIGUAL",
    "MENORIGUAL",
    "MAYOR",
    "MENOR",
    "DECIMAL",
    "ENTERO",
    "CADENA",
    "PTCOMA",
    "DOSPUNTOS",
    "ID",
    "ETIQUETA",
    "ASIG",
)

# Tokens
t_RABS = r"abs"
t_RMAIN = r"main"
t_RGOTO = r"goto"
t_RREAD = r"read"
t_REXIT = r"exit"
t_RUNSET = r"unset"
t_RPRINT = r"print"
t_RINT = r"int"
t_RFLOAT = r"float"
t_RCHAR = r"char"
t_RARRAY = r"array"
t_RXOR = r"xor"
t_RIF = r"if"
t_PARIZQ = r"\("
t_PARDER = r"\)"
t_CORIZQ = r"\["
t_CORDER = r"\]"
t_MAS = r"\+"
t_MENOS = r"-"
t_POR = r"\*"
t_DIVIDIDO = r"/"
t_MODULO = r"%"
t_RAND = r"&&"
t_ROR = r"\|\|"
t_RNOT = r"!"
t_RNOTBIT = r"~"
t_RORBIT = r"\|"
t_RANDBIT = r"&"
t_RXORBIT = r"\^"
t_SHIFTIZQ = r"<<"
t_SHIFTDER = r">>"
# t_IGUAL = r"=="
t_DIFERENTE = r"!="
t_MAYORIGUAL = r">="
t_MENORIGUAL = r"<="
t_MAYOR = r">"
t_MENOR = r"<"
t_PTCOMA = r";"
t_DOSPUNTOS = r":"
t_ASIG = r"\="

def t_IGUAL(t):
    """=="""
    return t


def t_DECIMAL(t):
    r"\d+\.\d+"
    try:
        t.value = float(t.value)
    except ValueError:
        print("Floaat value too large %d", t.value)
        t.value = 0
    return t


def t_ENTERO(t):
    r"\d+"
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_ID(t):
    r"[$][a-zA-Z]+[0-9]*"
    return t


def t_ETIQUETA(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    if t.value == "abs":
        t.type = "RABS"
        return t
    elif t.value == "array":
        t.type = "RARRAY"
        return t
    elif t.value == "print":
        t.type = "RPRINT"
        return t
    elif t.value == "unset":
        t.type = "RUNSET"
        return t
    elif t.value == "char":
        t.type = "RCHAR"
        return t
    elif t.value == "int":
        t.type = "RINT"
        return t
    elif t.value == "float":
        t.type = "RFLOAT"
        return t
    elif t.value == "goto":
        t.type = "RGOTO"
        return t
    elif t.value == "if":
        t.type = "RIF"
        return t
    elif t.value == "xor":
        t.type = "RXOR"
        return t
    elif t.value == "main":
        t.type = "RMAIN"
        return t
    elif t.value == "exit":
        t.type = "REXIT"
        return t
    elif t.value == "read":
        t.type = "RREAD"
        return t
    else:
        return t


def find_column(input, token):
    line_start = input.rfind(input, 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_CADENA(t):
    r"(\'|\").*?(\"|\')"
    t.value = t.value[1:-1]  # remuevo las comillas
    return t


# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r"\#.*\n"
    t.lexer.lineno += 1


# Caracteres ignorados
t_ignore = " \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    descripcion = "Caracter no reconocido por Agus: " + t.value[0]
    ErrorLexico = CError(descripcion, t.lexer.lineno, find_column('', t), "lexico")
    lErrores.append(ErrorLexico)
    t.lexer.skip(1)
