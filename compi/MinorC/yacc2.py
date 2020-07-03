from . import terminals

from compi.MinorC.lex2 import tokens
from compi.helpers.ast import ASTNode, LexToken
from compi.MinorC.globales2 import *


def find_column(inp: str, token: any):
    line_start = inp.rfind(inp, 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# Asociación de operadores y precedencia
precedence = (
    ('right', 'NOT'),
    ('left', 'AND', 'OR'),
    ('left', 'IGUAL', 'DIFERENTE'),
    ('left', 'MAYOR', 'MENOR'),
    ('left', 'MAYORIGUAL', 'MENORIGUAL', 'AUMENTO', 'DECREMENTO'),
    ('right', 'NOTBIT'),
    ('left', 'ANDBIT', 'ORBIT', 'XORBIT'),
    ('left', 'SHIFTIZQ', 'SHIFTDER'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    ('left', 'MODULO'),
    ('right', 'UMENOS')
)


# Definición de la gramática
def p_init(p):
    """ init : instrucciones"""
    r_shiftreduce_grammar.append(("Init", "instrucciones"))
    p[0] = ASTNode("init", p.lexer.lineno, 0, 0, p[1])


def p_instrucciones_lista(p):
    """instrucciones : instrucciones instruccion"""
    r_shiftreduce_grammar.append(("instrucciones", "instrucciones"))
    p[1].append(p[2])
    p[0] = p[1]


def p_instruccion_lista(p):
    """instrucciones    : instruccion"""
    r_shiftreduce_grammar.append(("instrucciones", "instruccion"))
    p[0] = ASTNode("instrucciones", p.lexer.lineno, 0, 0, p[1])


def p_instrucciones_evaluar(p):
    """instruccion : declaracion_registros PTCOMA
                    | asignacion_registros PTCOMA
                    | declaracion_structs PTCOMA
                    | declaracion_funciones
                    | sentencias_control
                    | funcion_print PTCOMA
                    | crear_struct PTCOMA"""
    r_shiftreduce_grammar.append(("instruccion", "sentencias"))
    p[0] = ASTNode("sentencias", p.lexer.lineno, 0, 0, p[1])


def p_instrucciones_error(p):
    """instruccion : error PTCOMA"""
    print("entro")
    r_shiftreduce_grammar.append(("error", "error"))
    p[0] = ASTNode("error", p.lexer.lineno, find_column(entrada, p.slice[2]))


def p_lista_sentencias(p):
    """lsentencias : lsentencias lsent"""
    r_shiftreduce_grammar.append(("sentencias", "sentencias"))
    p[1].append(p[2])
    p[0] = p[1]


def p_lista_sentencias2(p):
    """lsentencias : lsent"""
    r_shiftreduce_grammar.append(("sentencias", "sent"))
    p[0] = ASTNode("lsentencias", p.lexer.lineno, 0, 0, p[1])


def p_l_sent(p):
    """lsent : declaracion_registros PTCOMA
             | asignacion_registros PTCOMA
             | declaracion_structs PTCOMA
             | sentencias_control
             | funcion_print PTCOMA
             | sentencia_break PTCOMA
             | sentencia_continue PTCOMA
             | sentencia_return PTCOMA
             | callfuncion PTCOMA
             | sentencia_etiqueta
             | sentencia_goto"""
    r_shiftreduce_grammar.append(("lsent", "sentencia"))
    p[0] = p[1]  # ASTNode("lista_sentencias", p.lexer.lineno, 0, 0, p[1])


def p_crear_struct(p):
    """crear_struct : STRUCT ID LLAVEIZQ lsentencias LLAVEDER"""
    r_shiftreduce_grammar.append(("crear_struct", str(p[2])))
    a = ASTNode("linstr", p.lexer.lineno, 0, 0, *[j for j in p[4]])
    p[0] = ASTNode("creacion_struct", p.lexer.lineno, find_column(entrada, p.slice[2]), 0, ASTNode(p[2]), a)




def p_sentencias_control(p):
    """sentencias_control : sentencia_if
                          | sentencia_while
                          | sentencia_dowhile
                          | sentencia_switch
                          | sentencia_for"""
    r_shiftreduce_grammar.append(("sentencias_control", "flujos_control"))
    p[0] = ASTNode("sentencias_control", p.lexer.lineno, 0, 0, p[1])


def p_instrucciones_etiqueta(p):
    """sentencia_etiqueta : ID DOSPUNTOS"""
    r_shiftreduce_grammar.append(("sentencia_etiqueta", str(p[1])))
    p[0] = ASTNode("sentencia_etiqueta", p.lexer.lineno, find_column(entrada, p.slice[2]), 0, ASTNode(p[1]))


def p_instrucciones_goto(p):
    """sentencia_goto : GOTO ID PTCOMA"""
    r_shiftreduce_grammar.append(("sentencia_goto", str(p[2])))
    p[0] = ASTNode("sentencia_goto", p.lexer.lineno, find_column(entrada, p.slice[2]), 0, ASTNode(p[2]))


def p_sentencia_return(p):
    """sentencia_return : RETURN expresion"""
    r_shiftreduce_grammar.append(("sentencia_return", "return_expresion"))
    p[0] = ASTNode("sentencias_return", p.lexer.lineno, find_column(entrada, p.slice[1]), 0, p[2])


def p_sentencia_return2(p):
    """sentencia_return : RETURN"""
    r_shiftreduce_grammar.append(("sentencia_return", "return"))
    p[0] = ASTNode("sentencias_return", p.lexer.lineno, find_column(entrada, p.slice[1]))


def p_sentencia_break(p):
    """sentencia_break : BREAK"""
    r_shiftreduce_grammar.append(("sentencia_break", "break"))
    p[0] = ASTNode("sentencias_break", p.lexer.lineno, find_column(entrada, p.slice[1]), 0, ASTNode(p[1]))


def p_sentencia_continue(p):
    """sentencia_continue : CONTINUE"""
    r_shiftreduce_grammar.append(("sentencia_continue", "continue"))
    p[0] = ASTNode("sentencias_continue", p.lexer.lineno, find_column(entrada, p.slice[1]), 0, ASTNode(p[1]))


def p_sentencia_if(p):
    """sentencia_if : IF PARIZQ expresion PARDER LLAVEIZQ lsentencias LLAVEDER"""
    r_shiftreduce_grammar.append(("sentencia_if", "if_simple"))
    a = ASTNode("linstr", p.lexer.lineno, 0, 0, *[j for j in p[6]])
    p[0] = ASTNode("sentencia_if", p.lexer.lineno, find_column(entrada, p.slice[1]), 0, p[3], a)


def p_sentencia_else(t):
    """sentencia_if : IF PARIZQ expresion PARDER LLAVEIZQ lsentencias LLAVEDER ELSE LLAVEIZQ lsentencias LLAVEDER"""
    r_shiftreduce_grammar.append(("sentencia_if", "if_else"))
    a = ASTNode("linstr", t.lexer.lineno, 0, 0, *[i for i in t[6]])
    b = ASTNode("linstr", t.lexer.lineno, 0, 0, *[i for i in t[10]])
    t[0] = ASTNode("sentencia_if", t.lexer.lineno, find_column(entrada, t.slice[1]), 0, t[3], a, b)


def p_sentencia_else_if(t):
    """sentencia_if : IF PARIZQ expresion PARDER LLAVEIZQ lsentencias LLAVEDER ELSE sentencia_if"""
    r_shiftreduce_grammar.append(("sentencia_if", "if_else_if"))
    c = ASTNode("linstr", t.lexer.lineno, 0, 0, *[j for j in t[6]])
    t[0] = ASTNode("sentencia_if", t.lexer.lineno, find_column(entrada, t.slice[1]), 0, t[3], c, t[9])


def p_sentencia_switch(t):
    """sentencia_switch : SWITCH PARIZQ expresion PARDER LLAVEIZQ l_casos LLAVEDER"""
    r_shiftreduce_grammar.append(("sentencia_switch", "switch_no_default"))
    a = ASTNode("l_casos", t.lexer.lineno, 0, 0, *[j for j in t[6]])
    t[0] = ASTNode("sentencia_switch", t.lexer.lineno, find_column(entrada, t.slice[1]), 0, t[3], a)


def p_sentencia_switch_default(t):
    """sentencia_switch : SWITCH PARIZQ expresion PARDER LLAVEIZQ l_casos sentencia_default LLAVEDER"""
    r_shiftreduce_grammar.append(("sentencia_switch", "switch_default"))
    a = ASTNode("l_casos", t.lexer.lineno, 0, 0, *[j for j in t[6]])
    t[0] = ASTNode("sentencia_switch", t.lexer.lineno, find_column(entrada, t.slice[1]), 0, t[3], a, t[7])


def p_l_casos(t):
    """l_casos : l_casos casos"""
    r_shiftreduce_grammar.append(("l_casos", "l_casos"))
    t[1].append(t[2])
    t[0] = t[1]


def p_casos(t):
    """l_casos : casos"""
    r_shiftreduce_grammar.append(("l_casos", "casos"))
    t[0] = [t[1]]


def p_cases(t):
    """casos : CASE expresion DOSPUNTOS lsentencias"""
    r_shiftreduce_grammar.append(("casos", "case_expresion"))
    c = ASTNode("linstr", t.lexer.lineno, 0, 0, *[j for j in t[4]])
    t[0] = ASTNode("case", t.lexer.lineno, find_column(entrada, t.slice[1]), 0, t[2], c)


def p_sentencia_default(t):
    """sentencia_default : DEFAULT DOSPUNTOS lsentencias"""
    r_shiftreduce_grammar.append(("sentencia_default", "default"))
    a = ASTNode("linstr", t.lexer.lineno, 0, 0, *[j for j in t[3]])
    t[0] = ASTNode("default", t.lexer.lineno, find_column(entrada, t.slice[1]), 0, a)


def p_sentencia_for(t):
    """sentencia_for : FOR PARIZQ forinit PTCOMA expresion PTCOMA aum_dec PARDER LLAVEIZQ lsentencias LLAVEDER"""
    r_shiftreduce_grammar.append(("sentencia_for", "instrucciones"))
    a = ASTNode("linstr", t.lexer.lineno, 0, 0, *[j for j in t[10]])
    c = [t[3], t[5], t[7], a]
    t[0] = ASTNode("sentencia_for", t.lexer.lineno, find_column(entrada, t.slice[1]), 0, *c)


def p_forinit(t):
    """forinit : declaracion_registros
                | asignacion_registros"""
    r_shiftreduce_grammar.append(("forinit", "forinit_opcion"))
    t[0] = t[1]


def p_aum_dec(t):
    """aum_dec : ID AUMENTO
                | ID DECREMENTO"""
    r_shiftreduce_grammar.append(("aum_dec", str(t[1])))
    t[0] = ASTNode("aum_dec", t.lexer.lineno, find_column(entrada, t.slice[1]), 0, ASTNode(t[1]), ASTNode(t[2]))


def p_sentencia_while(t):
    """sentencia_while : WHILE PARIZQ expresion PARDER LLAVEIZQ lsentencias LLAVEDER"""
    r_shiftreduce_grammar.append(("sentencia_while", "while"))
    c = ASTNode("linstr", t.lexer.lineno, 0, 0, *[j for j in t[6]])
    t[0] = ASTNode("sentencia_while", t.lexer.lineno, find_column(entrada, t.slice[1]), t[3], c)


def p_sentencia_dowhile(t):
    """sentencia_dowhile : DO LLAVEIZQ lsentencias LLAVEDER WHILE PARIZQ expresion PARDER PTCOMA"""
    r_shiftreduce_grammar.append(("sentencia_dowhile", "do_while"))
    n = ASTNode("linstr", t.lexer.lineno, 0, 0, *[j for j in t[3]])
    t[0] = ASTNode("sentencia_dowhile", t.lexer.lineno, find_column(entrada, t.slice[1]), 0, n, t[7])


def p_declaracion_funciones(t):
    """declaracion_funciones : tipo_variable ID PARIZQ PARDER LLAVEIZQ lsentencias LLAVEDER"""
    r_shiftreduce_grammar.append(("declaracion_funciones", str(t[2])))
    aux = ASTNode("param_func", t.lexer.lineno, 0)
    aux2 = ASTNode("linstr", t.lexer.lineno, 0, 0, *[j for j in t[6]])
    c = [t[1], ASTNode(t[2]), aux, aux2]
    t[0] = ASTNode("declaracion_funcion", t.lexer.lineno, find_column(entrada, t.slice[2]), 0, *c)


def p_declaracion_funcion2(t):
    """declaracion_funciones : tipo_variable ID PARIZQ lista_params PARDER LLAVEIZQ lsentencias LLAVEDER """
    r_shiftreduce_grammar.append(("declaracion_funciones", str(t[2])))
    aux = ASTNode("param_func", t.lexer.lineno, 0, 0, *[i for i in t[4]])
    aux2 = ASTNode("linstr", t.lexer.lineno, 0, 0, *[j for j in t[7]])
    c = [t[1], ASTNode(t[2]), aux, aux2]
    t[0] = ASTNode("declaracion_funcion", t.lexer.lineno, find_column(entrada, t.slice[2]), 0, *c)


def p_declaracoin_funcionmain(t):
    """declaracion_funciones : INT MAIN PARIZQ PARDER LLAVEIZQ lsentencias LLAVEDER"""
    r_shiftreduce_grammar.append(("declaracion_funciones", "main"))
    aux = ASTNode("linstr", t.lexer.lineno, 0, 0, *[j for j in t[6]])
    t[0] = ASTNode("declaracion_funcion", t.lexer.lineno, find_column(entrada, t.slice[1]), 0, ASTNode(t[1]), ASTNode(t[2]), aux)


def p_lista_params(t):
    """lista_params : lista_params COMA l_param"""
    r_shiftreduce_grammar.append(("lista_params", "lista_params"))
    t[1].append(t[3])
    t[0] = t[1]


def p_lista_params2(t):
    """lista_params : l_param"""
    r_shiftreduce_grammar.append(("lista_params", "l_param"))
    t[0] = [t[1]]


def p_l_param(t):
    """l_param : tipo_variable ID
                | STRUCT ID declar_opcion"""
    r_shiftreduce_grammar.append(("l_param", "tipo_parametro"))
    if t[1] == 'struct':
        t[0] = ASTNode("l_param", t.lexer.lineno, find_column(entrada, t.slice[2]), 0, ASTNode(t[2]), t[3])
    else:
        t[0] = ASTNode("l_param", t.lexer.lineno, find_column(entrada, t.slice[2]), 0, t[1], ASTNode(t[2]))


def p_funcion_print(t):
    """funcion_print : PRINT PARIZQ CADENA COMA l_expresion PARDER"""
    r_shiftreduce_grammar.append(("funcion_print", "print_double_parameter"))
    aux = ASTNode("l_expresiones", t.lexer.lineno, 0, None, *[i for i in t[5]])
    t[0] = ASTNode("print", t.lexer.lineno, find_column(entrada, t.slice[1]), None, ASTNode(t[3]), aux)


def p_funcion_print2(t):
    """funcion_print : PRINT PARIZQ CADENA PARDER"""
    r_shiftreduce_grammar.append(("funcion_print", "print_normal"))
    t[0] = ASTNode("print", t.lexer.lineno, find_column(entrada, t.slice[1]), None, ASTNode(t[3]))


def p_declaracion_structs(t):
    """declaracion_structs : STRUCT ID declar_opcion"""
    t[0] = ASTNode("declaracion_structs", t.lexer.lineno, find_column(entrada, t.slice[1]), None, ASTNode(t[1]), t[3])


def p_declaracion_registros(t):
    """declaracion_registros : tipo_variable lista_ids"""
    r_shiftreduce_grammar.append(("declaracion_registros", "declaracion_variable"))
    aux2 = ASTNode("lista_ids", t.lexer.lineno, 0, None, *[j for j in t[2]])
    t[0] = ASTNode("declaracion_registros", t.lexer.lineno, 0, None, t[1], aux2)


def p_asignacion_registros(t):
    """asignacion_registros : ID lopcion_asignacion tipos_asignacion expresion"""
    r_shiftreduce_grammar.append(("asignacion_registros", str(t[1])))
    aux = ASTNode("l_opcion_asig", t.lexer.lineno, 0, None, *[i for i in t[2]])
    childs = [ASTNode(t[1]), aux, t[3], t[4]]
    t[0] = ASTNode("asignacion_registros", t.lexer.lineno, 0, None, childs)


def p_asignacion_registros2(t):
    """asignacion_registros : ID tipos_asignacion expresion"""
    r_shiftreduce_grammar.append(("asignacion_registros", str(t[1])))
    t[0] = ASTNode("asignacion_registros", t.lexer.lineno, 0, None, ASTNode(t[1]), t[2], t[3])


def p_oplasig(t):
    """lopcion_asignacion : lopcion_asignacion opcion_asignacion"""
    t[1].append(t[2])
    t[0] = t[1]


def p_oplasig2(t):
    """lopcion_asignacion : opcion_asignacion"""
    t[0] = [t[1]]


def p_opcion_asignacion(t):
    """opcion_asignacion : CORIZQ expresion CORDER"""
    r_shiftreduce_grammar.append(("opciones_asignacion", "tipo_array"))
    t[0] = ASTNode("acceso_modificacion", t.lexer.lineno, 0, None, t[2])


def p_opcion_asignacion_dot_id(t):
    """opcion_asignacion : PUNTO ID"""
    r_shiftreduce_grammar.append(("opciones_asignacion", str(t[2])))
    t[0] = ASTNode("acceso_modificacion2", t.lexer.lineno, 0, None, ASTNode(t[2]))


def p_lista_ids(t):
    """lista_ids : lista_ids COMA declar_opcion"""
    t[1].append(t[3])
    t[0] = t[1]


def p_lista_ids2(t):
    """lista_ids : declar_opcion"""
    t[0] = [t[1]]


def p_declar_opcion(t):
    """declar_opcion : ID"""
    r_shiftreduce_grammar.append(("declar_opcion", str(t[1])))
    t[0] = ASTNode("tipo_declaracion", t.lexer.lineno, find_column(entrada, t.slice[1]), None, ASTNode(t[1]))


def p_declar_opcion2(t):
    """declar_opcion : ID tipos_asignacion expresion"""
    childs = [ASTNode(t[1]), t[2], t[3]]
    r_shiftreduce_grammar.append(("declar_opcion", str(t[1])))
    t[0] = ASTNode("tipo_declaracion2", t.lexer.lineno, find_column(entrada, t.slice[1]), None, *childs)


def p_declar_opcion3(t):
    """declar_opcion : ID CORIZQ CORDER"""
    r_shiftreduce_grammar.append(("declar_opcion", str(t[1])))
    t[0] = ASTNode("tipo_declaracion3", t.lexer.lineno, find_column(entrada, t.slice[1]), None, ASTNode(t[1]))


def p_declar_opcion4(t):
    """declar_opcion : ID CORIZQ expresion CORDER"""
    r_shiftreduce_grammar.append(("declar_opcion", str(t[1])))
    t[0] = ASTNode("tipo_declaracion4", t.lexer.lineno, find_column(entrada, t.slice[1]), None, ASTNode(t[1]), t[3])


def p_declar_opcion5(t):
    """declar_opcion : ID CORIZQ CORDER tipos_asignacion expresion"""
    childs = [
        ASTNode(t[1]),
        t[4],
        t[5],
    ]
    r_shiftreduce_grammar.append(("declar_opcion", str(t[1])))
    t[0] = ASTNode("tipo_declaracion5", t.lexer.lineno, find_column(entrada, t.slice[1]), None, *childs)


def p_declar_opcion6(t):
    """declar_opcion : ID CORIZQ expresion CORDER tipos_asignacion expresion"""
    childs = [
        ASTNode(t[1]),
        t[3],
        t[5],
        t[6]
    ]
    r_shiftreduce_grammar.append(("declar_opcion", str(t[1])))
    t[0] = ASTNode("tipo_declaracion6", t.lexer.lineno, find_column(entrada, t.slice[1]), None, *childs)


def p_tipos_asignacion(t):
    """tipos_asignacion : ASIG
                        | ASIGMAS
                        | ASIGMENOS
                        | ASIGPOR
                        | ASIGDIV
                        | ASIGMODULO
                        | ASIGSHIFTIZQ
                        | ASIGSHITFDER
                        | ASIGAND
                        | ASIGOR
                        | ASIGXOR"""
    r_shiftreduce_grammar.append(("tipo_asignacion", str(t[1])))
    t[0] = ASTNode("tipo_asignacion", t.lexer.lineno, find_column(entrada, t.slice[1]), None, ASTNode(t[1]))


def p_tipo_variable(t):
    """tipo_variable : DOUBLE
                    | INT
                    | FLOAT
                    | CHAR
                    | VOID"""
    r_shiftreduce_grammar.append(("tipo_variable", str(t[1])))
    t[0] = ASTNode("tipo_variable", t.lexer.lineno, find_column(entrada, t.slice[1]), None, ASTNode(t[1]))


def p_expresion_binaria(t):
    """expresion : expresion MAS expresion
                  | expresion MENOS expresion
                  | expresion POR expresion
                  | expresion DIVIDIDO expresion
                  | expresion MODULO expresion
                  | expresion AND expresion
                  | expresion OR expresion
                  | expresion MAYOR expresion
                  | expresion MENOR expresion
                  | expresion MAYORIGUAL expresion
                  | expresion MENORIGUAL expresion
                  | expresion IGUAL expresion
                  | expresion DIFERENTE expresion
                  | expresion ANDBIT expresion
                  | expresion ORBIT expresion
                  | expresion XORBIT expresion
                  | expresion SHIFTIZQ expresion
                  | expresion SHIFTDER expresion"""
    r_shiftreduce_grammar.append(("expresion", str(t[2])))
    t[0] = ASTNode(t[2], t.lexer.lineno, find_column(entrada, t.slice[2]), None, t[1], t[3])


def p_expresion_unaria(t):
    """expresion : MENOS expresion %prec UMENOS
                  | NOT expresion
                  | NOTBIT expresion"""
    r_shiftreduce_grammar.append(("expresion", str(t[1])))
    t[0] = ASTNode("expresion_unaria", t.lexer.lineno, find_column(entrada, t.slice[1]), None, ASTNode(t[1]), t[2])


def p_expresion_callfunc(t):
    """expresion : callfuncion"""
    r_shiftreduce_grammar.append(("expresion", "callfuncion"))
    t[0] = ASTNode("expresion_callfuncion", t.lexer.lineno, 0, None, t[1])


def p_expresion_casteo(t):
    """expresion : PARIZQ tipo_variable PARDER expresion"""
    r_shiftreduce_grammar.append(("expresion", "expresion_casteo"))
    t[0] = ASTNode("expresion_casteo", t.lexer.lineno, 0, None, t[2], t[4])


def p_expresion_llamada_funcion(t):
    """callfuncion : ID PARIZQ l_expresion PARDER"""
    r_shiftreduce_grammar.append(("call_funcion", str(t[1])))
    childs = [ASTNode(t[1]), ASTNode("l_expresiones", t.lexer.lineno, 0, 0, *[i for i in t[3]])]
    t[0] = ASTNode("call_funcion", t.lexer.lineno, find_column(entrada, t.slice[1]), None, *childs)


def p_expresion_llamada_funcionsinparam(t):
    """callfuncion : ID PARIZQ PARDER"""
    r_shiftreduce_grammar.append(("call_funcion", str(t[1])))
    t[0] = ASTNode("call_funcion", t.lexer.lineno, find_column(entrada, t.slice[1]), None, ASTNode(t[1]))


def p_expresion_agrupacion(t):
    """expresion : PARIZQ expresion PARDER"""
    r_shiftreduce_grammar.append(("expresion", "expresion_agrupacion"))
    t[0] = ASTNode("expresion_agrup", t.lexer.lineno, find_column(entrada, t.slice[1]), None, t[2])


def p_expresion_ternario(t):
    """expresion : expresion_ternario"""
    t[0] = t[1]


def p_ternario(t):
    """expresion_ternario : expresion TERNARIO expresion DOSPUNTOS expresion"""
    childs = [ASTNode(t[1]), ASTNode(t[3]), ASTNode(t[5])]
    t[0] = ASTNode("expresion_ternario", t.lexer.lineno, find_column(entrada, t.slice[2]), None, *childs)


def p_expresion_number(t):
    """expresion    : ENTERO
                    | DECIMAL
                    | CADENA"""
    r_shiftreduce_grammar.append(("expresion_number", str(t[1])))
    t[0] = ASTNode("expresion_number", t.lexer.lineno, find_column(entrada, t.slice[1]), None, ASTNode(t[1]))


def p_expresion_ids(t):
    """expresion : ID"""
    r_shiftreduce_grammar.append(("expresion_id", str(t[1])))
    t[0] = ASTNode("expresion_id", t.lexer.lineno, find_column(entrada, t.slice[1]), None, ASTNode(t[1]))


def p_expresion_aumdec(t):
    """expresion : expresion aumento_decremento"""
    r_shiftreduce_grammar.append(("expresion_aumdec", "aum_dec"))
    t[0] = ASTNode("aum_dec", t.lexer.lineno, 0, None, t[1], t[2])


def p_expresion_scanf(t):
    """expresion : SCANF PARIZQ PARDER"""
    r_shiftreduce_grammar.append(("expresion", str(t[1])))
    t[0] = ASTNode("scanf", t.lexer.lineno, find_column(entrada, t.slice[1]), None, ASTNode(t[1]))


def p_expresion_acceso_array(t):
    """expresion : ID lista_accesos"""
    childs = [
        ASTNode(t[1]),
        ASTNode("l_acceso", t.lexer.lineno, 0, None, *[i for i in t[2]])
    ]
    t[0] = ASTNode("acceso", t.lexer.lineno, find_column(entrada, t.slice[1]), None, childs)


def p_expresion_listaacceso(t):
    """lista_accesos : lista_accesos lacceso"""
    t[1].append(t[3])
    t[0] = t[1]


def p_expresion_lista_lacceso(t):
    """lista_accesos : lacceso"""
    t[0] = [t[1]]


def p_expresion_lacceso(t):
    """lacceso : CORIZQ expresion CORDER"""
    t[0] = ASTNode("tipo_acceso2", t.lexer.lineno, find_column(entrada, t.slice[1]), None, t[2])


def p_expresion_lacceso2(t):
    """lacceso : PUNTO ID"""
    t[0] = ASTNode("tipo_acceso1", t.lexer.lineno, find_column(entrada, t.slice[1]), None, ASTNode(t[2]))


def p_expresion_valores_array(t):
    """expresion : LLAVEIZQ l_expresion LLAVEDER"""
    aux = ASTNode("l_expresiones", t.lexer.lineno, 0, None, *[i for i in t[2]])
    t[0] = ASTNode("valores_array", t.lexer.lineno, find_column(entrada, t.slice[1]), None, aux)


def p_expresion_aumentodecremento(t):
    """aumento_decremento : AUMENTO
                            | DECREMENTO"""
    t[0] = ASTNode(t[1], t.lexer.lineno, find_column(entrada, t.slice[1]))


def p_l_expresion(t):
    """l_expresion : l_expresion COMA expresion"""
    t[1].append(t[3])
    t[0] = t[1]


def p_lexpresion(t):
    """l_expresion : expresion"""
    t[0] = [t[1]]


def p_error(p):
    d = "Error gramatical en: " + str(p.value)
    print(d)
    lErrores.append(CError(d, p.lexer.lineno, find_column(entrada, p), "sintactico"))