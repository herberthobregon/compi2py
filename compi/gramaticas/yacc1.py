from compi.gramaticas.lex1 import tokens
from compi.helpers.ast import ASTNode, LexToken
from compi.gramaticas.globales import *


def find_column(inp: str, token: any):
    line_start = inp.rfind(inp, 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# Asociación de operadores y precedencia
precedence = (
    ("right", "RNOT"),
    ("left", "RAND", "ROR", "ETIQUETA"),
    ("left", "IGUAL", "DIFERENTE"),
    ("left", "MAYOR", "MENOR"),
    ("left", "MAYORIGUAL", "MENORIGUAL"),
    ("right", "RNOTBIT"),
    ("left", "RANDBIT", "RORBIT", "RXORBIT"),
    ("left", "SHIFTIZQ", "SHIFTDER"),
    ("left", "MAS", "MENOS"),
    ("left", "POR", "DIVIDIDO"),
    ("left", "MODULO", "RABS"),
    ("right", "UMENOS"),
)


def p_init(t):
    """ initGram : RMAIN DOSPUNTOS instrucciones"""
    init_ast = ASTNode("start", t.lexer.lineno, find_column(entrada, t.slice[1]), None, t[3])
    init_ast.childs = t[3]
    t[0] = init_ast


def p_instructions_list(t):
    """instrucciones    : instrucciones instruccion"""
    t[1].append(t[2])
    t[0] = t[1]


def p_instructions_list_1(t):
    """instrucciones    : instruccion"""
    t[0] = [t[1]]


def p_instructions_eval(t):
    """instruccion : declaracion_registros PTCOMA
                    | funcion_print PTCOMA
                    | funcion_unset PTCOMA
                    | salto_condicional PTCOMA
                    | instruccion_control PTCOMA"""
    t[0] = t[1]


def p_instruction_exit(t):
    """instruccion : REXIT PTCOMA"""
    t[0] = ASTNode(t[1], t.lexer.lineno, find_column(entrada, t.slice[2]))


def p_instructions_error(t):
    """instruccion : error PTCOMA"""
    NodoSentencias = ASTNode("error", t.lexer.lineno, find_column(entrada, t.slice[2]))
    t[0] = NodoSentencias


# print("Error sintáctico en '%s'" % t.value)


def p_instructions_tag(t):
    """instruccion : ETIQUETA DOSPUNTOS"""
    t[0] = ASTNode("etiqueta", t.lexer.lineno, find_column(entrada, t.slice[1]), None, ASTNode(t[1]))


def p_salto_condicional(t):
    """salto_condicional : RGOTO ETIQUETA"""
    NodoSaltoCond = ASTNode(
        "salto_incondicional", t.lexer.lineno, find_column(entrada, t.slice[1])
    )
    NodoSaltoCond.add_child(ASTNode(t[2]))
    t[0] = NodoSaltoCond


def p_instruccion_control(t):
    """instruccion_control : RIF PARIZQ expresion PARDER RGOTO ETIQUETA"""
    NodoControl = ASTNode(
        "sentencia_control", t.lexer.lineno, find_column(entrada, t.slice[1])
    )
    NodoControl.add_child(t[3])
    NodoControl.add_child(ASTNode(t[6]))
    t[0] = NodoControl


def p_funcion_unset(t):
    """funcion_unset : RUNSET PARIZQ expresion PARDER"""
    NodoUnset = ASTNode("unset", t.lexer.lineno, find_column(entrada, t.slice[1]))
    NodoUnset.add_child(t[3])
    t[0] = NodoUnset


def p_funcion_print(t):
    """funcion_print : RPRINT PARIZQ expresion PARDER"""
    NodoUnset = ASTNode("print", t.lexer.lineno, find_column(entrada, t.slice[1]))
    NodoUnset.add_child(t[3])
    t[0] = NodoUnset


def p_declaracion_registros(t):
    """declaracion_registros : ID ASIG expresion"""
    NodoDeclaracion = ASTNode(
        "declaracion_asignacion", t.lexer.lineno, find_column(entrada, t.slice[1])
    )
    NodoDeclaracion.add_child(ASTNode(t[1]))
    NodoDeclaracion.add_child(t[3])
    t[0] = NodoDeclaracion


def p_declaracion_arraymod(t):
    """declaracion_registros : otra ASIG expresion"""
    NodoDeclaracion = ASTNode(
        "declaracion_asignacion", t.lexer.lineno, find_column(entrada, t.slice[2])
    )
    NodoDeclaracion.add_child(t[1])
    NodoDeclaracion.add_child(t[3])
    t[0] = NodoDeclaracion


def p_otra(t):
    """otra : ID lista_accesos"""
    NodoModificacion = ASTNode(
        "modificar_array", t.lexer.lineno, find_column(entrada, t.slice[1])
    )
    NodoModificacion.add_child(ASTNode(t[1]))
    NodoModificacion.add_child(t[2])
    t[0] = NodoModificacion


def p_expresion_binaria(t):
    """expresion :  expresion MAS expresion
                    | expresion MENOS expresion
                    | expresion POR expresion
                    | expresion DIVIDIDO expresion
                    | expresion MODULO expresion
                    | expresion RAND expresion
                    | expresion ROR expresion
                    | expresion RXOR expresion
                    | expresion MAYOR expresion
                    | expresion MENOR expresion
                    | expresion MAYORIGUAL expresion
                    | expresion MENORIGUAL expresion
                    | expresion IGUAL expresion
                    | expresion DIFERENTE expresion
                    | expresion RANDBIT expresion
                    | expresion RORBIT expresion
                    | expresion RXORBIT expresion
                    | expresion SHIFTIZQ expresion
                    | expresion SHIFTDER expresion"""
    t[0] = ASTNode(t[2], t.lexer.lineno, find_column(entrada, t.slice[2]), None, t[1], t[3])


def p_casteos(t):
    """casteos : PARIZQ tipo_casteo PARDER expresion"""
    NodoCasteo = ASTNode("casteos", t.lexer.lineno, find_column(entrada, t.slice[1]))
    NodoCasteo.add_child(t[2])
    NodoCasteo.add_child(t[4])
    t[0] = NodoCasteo


def p_tipo_casteo(t):
    """tipo_casteo : RINT
                    | RFLOAT
                    | RCHAR """
    NodoCasteo = ASTNode("tipo_casteo", t.lexer.lineno, find_column(entrada, t.slice[1]))
    NodoauxCast = ASTNode(t[1], t.lexer.lineno, find_column(entrada, t.slice[1]))
    NodoCasteo.add_child(NodoauxCast)
    t[0] = NodoCasteo


def p_valor_absoluto(t):
    """absValue : RABS PARIZQ expresion PARDER"""
    NodoAbs = ASTNode("absoluto", t.lexer.lineno, find_column(entrada, t.slice[1]))
    NodoAbs.add_child(t[3])
    t[0] = NodoAbs


def p_lista_de_accesos(t):
    """lista_accesos : lista_accesos CORIZQ expresion CORDER"""
    NodoAuxLAcceso = t[1]
    NodoRest = t[3]
    NodoAuxLAcceso.add_child(NodoRest)
    t[0] = NodoAuxLAcceso


def p_l_de_accesos(t):
    """lista_accesos : CORIZQ expresion CORDER"""
    NodoLAcceso = ASTNode("lista_acceso", t.lexer.lineno, find_column(entrada, t.slice[1]))
    NodoLAcceso.add_child(t[2])
    t[0] = NodoLAcceso


def p_expresion_unaria(t):
    """expresion : MENOS expresion %prec UMENOS
                  | RNOT expresion
                  | RNOTBIT expresion"""
    NodoExpresionUnaria = ASTNode(
        "expresion_unaria", t.lexer.lineno, find_column(entrada, t.slice[1])
    )
    NodoExpresionUnaria.add_child(ASTNode(t[1]))
    NodoExpresionUnaria.add_child(t[2])
    t[0] = NodoExpresionUnaria


def p_expresion_agrupacion(t):
    "expresion : PARIZQ expresion PARDER"
    NodoExpresionAgrupar = ASTNode(
        "exp_agrupacion", t.lexer.lineno, find_column(entrada, t.slice[1])
    )
    NodoExpresionAgrupar.add_child(t[2])
    t[0] = NodoExpresionAgrupar


def p_expresion_number(t):
    """expresion    : ENTERO
                    | DECIMAL
                    | ID
                    | CADENA
                    | RABS PARIZQ expresion PARDER
                    | RARRAY PARIZQ PARDER
                    | RREAD PARIZQ PARDER"""
    if t[1] == "abs":
        t[0] = ASTNode(
            "abs", t.lexer.lineno, find_column(entrada, t.slice[1]), None, t[3]
        )
    else:
        t[0] = ASTNode(
            "expresion_number", t.lexer.lineno, find_column(entrada, t.slice[1]), None, ASTNode(t[1])
        )


def p_expresion_casteo(t):
    """expresion : casteos"""
    NodoExpresionNumber = ASTNode("expresion_number", t.lexer.lineno, 0)
    NodoExpresionNumber.add_child(t[1])
    t[0] = NodoExpresionNumber


def p_exp_accesoArray(t):
    """expresion : accesos_array"""
    NodoExpresionNumber = ASTNode("expresion_number", t.lexer.lineno, 0)
    Nodoaux = t[1]
    NodoExpresionNumber.add_child(Nodoaux)
    t[0] = NodoExpresionNumber


def p_acceso_arrayExp(t):
    """accesos_array : ID lista_accesos"""
    NodoAccesArray = ASTNode(
        "access_arrayexp", t.lexer.lineno, find_column(entrada, t.slice[1])
    )
    NodoAccesArray.add_child(ASTNode(t[1]))
    NodoAccesArray.add_child(t[2])
    t[0] = NodoAccesArray


def p_error(t: LexToken):
    try:
        descripcion = "Error gramatical en: " + t.value
    except:
        descripcion = 'Error gramatical en: ;'
    ErrorSintactico = CError(
        descripcion, t.lexer.lineno, find_column(entrada, t), "sintactico"
    )
    lErrores.append(ErrorSintactico)
