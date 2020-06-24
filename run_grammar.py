import ply.lex
import ply.yacc
from graphviz import Source
from compi.helpers.ast import ASTNode
from compi.gramaticas import lex1, yacc1, globales
from PyQt5 import QtWidgets, QtCore, QtGui
from typing import Optional, List
import re

cnx: Optional[QtWidgets.QWidget] = None
console_handler: Optional[any] = None
next_ats: Optional[ASTNode] = None


def get_ast(txt: str, cnxx: any, console_handlerx: any) -> ASTNode:
    global cnx, console_handler
    console_handler = console_handlerx
    cnx = cnxx
    lexer = ply.lex.lex(module=lex1)
    parser = ply.yacc.yacc(module=yacc1, tabmodule="yacc1_tab")
    root: ASTNode = parser.parse(txt)  # the input

    dot = Source(root.to_str())
    dot.format = 'png'
    dot.render('graph')

    lista = root.genarar_lista()
    run(lista)
    print("\n".join([str(i) for i in globales.sym_table]))
    parser.restart()
    return root


def debug_ast(txt: str, cnxx: any, console_handlerx: any) -> ASTNode:
    global cnx, console_handler, next_ats
    console_handler = console_handlerx
    cnx = cnxx
    lexer = ply.lex.lex(module=lex1)
    parser = ply.yacc.yacc(module=yacc1, tabmodule="yacc1_tab")
    root: ASTNode = parser.parse(txt)  # the input

    dot = Source(root.to_str())
    dot.format = 'png'
    dot.render('graph')

    lista = root.genarar_lista()
    next_ats = debug(lista)
    return next_ats


def step():
    global cnx, console_handler, next_ats
    next_ats = debug(next_ats)
    return next_ats


def evaluar_ast(value: ASTNode):
    if isinstance(value, float) or isinstance(value, int):
        return value
    elif isinstance(value, str):
        if '$' in value:
            return get_id(value)
        elif value == 'read':
            inn, ok = QtWidgets.QInputDialog.getText(cnx, "read()", "Ingrese un valor")
            if re.match('[0-9]+$', inn):
                return int(inn)
            elif re.match(r'[0-9]+.[0-9]+$', inn):
                return float(inn)
            else:
                return str(inn).strip()
        else:
            return str(value)

    return 1


def get_id(value):
    rsp = list(filter(lambda x: (x.key == value), globales.sym_table))
    if len(rsp) > 0:
        return rsp[0].value
    return None


def eval_expression(root: ASTNode):
    typee = root.typee
    exp_val = None

    if typee == '+':
        exp_val = eval_plus(root.childs)
    elif typee == '-':
        exp_val = eval_minus(root.childs)
    elif typee == '*':
        exp_val = eval_multi(root.childs)
    elif typee == '/':
        exp_val = eval_div(root.childs)
    elif typee == '%':
        exp_val = eval_mod(root.childs)
    elif typee == '&&':
        exp_val = eval_and(root.childs)
    elif typee == '||':
        exp_val = eval_or(root.childs)
    elif typee == 'xor':
        exp_val = eval_xor(root.childs)
    elif typee == '<':
        exp_val = eval_lt(root.childs)
    elif typee == '>':
        exp_val = eval_gt(root.childs)
    elif typee == '<=':
        exp_val = eval_lte(root.childs)
    elif typee == '>=':
        exp_val = eval_gte(root.childs)
    elif typee == '==':
        exp_val = eval_equal(root.childs)
    elif typee == '!=':
        exp_val = eval_diff(root.childs)
    elif typee == '&':
        exp_val = eval_and_bit(root.childs)
    elif typee == '|':
        exp_val = eval_or_bit(root.childs)
    elif typee == '^':
        exp_val = eval_xor_bit(root.childs)
    elif typee == '<<':
        exp_val = eval_shift_izq(root.childs)
    elif typee == '>>':
        exp_val = eval_shift_der(root.childs)
    elif typee == 'abs':
        exp_val = eval_abs(root.childs)
    elif typee == 'expresion_number':
        data = root.childs[0].typee
        if data == 'access_arrayexp':
            exp_val = eval_expression(root.childs[0])
        elif data == 'casteos':
            exp_val = cast_value(root.childs)
        elif data == 'array':
            exp_val = {}
        else:
            exp_val = evaluar_ast(data)
    elif typee == 'access_arrayexp':
        key = root.childs[0].typee
        lista = root.childs[1]
        p_list = []
        for node in lista.childs:
            v = eval_expression(node)
            p_list.append(v)
        schema = get_id(key) or {}
        for i in range(0, len(p_list) - 1):
            elem = p_list[i]
            if schema.get(elem) is None:
                schema[elem] = {}
            schema = schema[elem]
        if schema is not None:
            exp_val = schema[p_list[len(p_list) - 1]]
    elif typee == 'expresion_unaria':
        exp_val = eval_unaria(root.childs)
    elif typee == 'exp_agrupacion':
        exp_val = eval_expression(root.childs[0])

    return exp_val


def cast_value(childs: List[ASTNode]):
    izq = childs[0].childs[0].childs[0].typee
    der = eval_expression(childs[0].childs[1])
    try:
        if izq == 'float':
            return float(der)
        if izq == 'int':
            try:
                intt = int(der)
                return intt
            except:
                intt = ord(der)
                return intt
        if izq == 'char':
            return chr(der)
    except Exception as e:
        ne = globales.CError("Error al operar casteo ({}) {}".format(izq, der), childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_plus(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    is_number = (isinstance(izq, int) or isinstance(izq, float)) and (isinstance(der, int) or isinstance(der, float))
    is_str = isinstance(izq, str) and isinstance(der, str)
    if is_number:
        resultado = izq + der
        return resultado
    elif is_str:
        resultado = izq + der
        return str(resultado)
    else:
        ne = globales.CError("Error al operar la suma", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_minus(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    is_number = (isinstance(izq, int) or isinstance(izq, float)) and (isinstance(der, int) or isinstance(der, float))
    is_str = isinstance(izq, str) and isinstance(der, str)
    if is_number:
        resultado = izq - der
        return resultado
    elif is_str:
        resultado = izq - der
        return str(resultado)
    else:
        ne = globales.CError("Error al operar la resta", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_multi(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    is_number = (isinstance(izq, int) or isinstance(izq, float)) and (isinstance(der, int) or isinstance(der, float))
    is_str = isinstance(izq, str) and isinstance(der, str)
    if is_number:
        resultado = izq * der
        return resultado
    else:
        ne = globales.CError("Error al operar la multi", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_div(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    is_number = (isinstance(izq, int) or isinstance(izq, float)) and (isinstance(der, int) or isinstance(der, float))
    is_str = isinstance(izq, str) and isinstance(der, str)

    try:
        if is_number:
            resultado = izq / der
            return resultado
        else:
            ne = globales.CError("Error al operar la div", childs[0].line, 0, "semantico")
            globales.lErroresSemanticos.append(ne)
            console_handler('Error de operandos')
    except:
        ne = globales.CError("Error al operar la div", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_mod(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    is_number = (isinstance(izq, int) or isinstance(izq, float)) and (isinstance(der, int) or isinstance(der, float))
    is_str = isinstance(izq, str) and isinstance(der, str)
    if is_number:
        resultado = izq % der
        return resultado
    else:
        ne = globales.CError("Error al operar module", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_and(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    try:
        return 1 if izq and der else 0
    except Exception as e:
        ne = globales.CError("Error al operar la AND", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_or(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    try:
        return 1 if izq or der else 0
    except Exception as e:
        ne = globales.CError("Error al operar OR", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_xor(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    try:
        return 1 if izq ^ der else 0
    except Exception as e:
        ne = globales.CError("Error al operar XOR", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_lt(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    try:
        return 1 if izq < der else 0
    except Exception as e:
        ne = globales.CError("Error al operar la LT", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_gt(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    try:
        return 1 if izq > der else 0
    except Exception as e:
        ne = globales.CError("Error al operar la GT", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_lte(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    try:
        return 1 if izq <= der else 0
    except Exception as e:
        ne = globales.CError("Error al operar la LTE", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_gte(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    try:
        return 1 if izq >= der else 0
    except Exception as e:
        ne = globales.CError("Error al operar la GTE", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_equal(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    try:
        return 1 if izq == der else 0
    except Exception as e:
        ne = globales.CError("Error al operar la suma", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_diff(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    try:
        return 1 if izq != der else 0
    except Exception as e:
        ne = globales.CError("Error al operar la suma", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_and_bit(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    try:
        return izq & der
    except Exception as e:
        ne = globales.CError("Error al operar la AND_BIT", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_or_bit(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    try:
        return izq | der
    except Exception as e:
        ne = globales.CError("Error al operar la OR_BIT", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_xor_bit(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    try:
        return izq ^ der
    except Exception as e:
        ne = globales.CError("Error al operar la XOR", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_shift_izq(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    try:
        return izq << der
    except Exception as e:
        ne = globales.CError("Error al operar la suma", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_shift_der(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    der = eval_expression(childs[1])
    try:
        return izq >> der
    except Exception as e:
        ne = globales.CError("Error al operar la suma", childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_abs(childs: List[ASTNode]):
    izq = eval_expression(childs[0])
    try:
        return abs(izq)
    except Exception as e:
        ne = globales.CError("Error al operar la abs({})".format(izq), childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def eval_unaria(childs: List[ASTNode]):
    izq = childs[0].typee
    der = eval_expression(childs[1])
    try:
        if izq == '!':
            return 0 if der else 1
        elif izq == '-':
            return der * -1
        elif izq == '~':
            return ~der
    except Exception as e:
        ne = globales.CError("Error al operar la -({})".format(izq), childs[0].line, 0, "semantico")
        globales.lErroresSemanticos.append(ne)
        console_handler('Error de operandos')


def e_unset(key: int):
    rsp = list(filter(lambda x: (x.key != key), globales.sym_table))
    globales.sym_table = rsp


def eval_modificar_array(root: ASTNode, value: any):
    typee = root.typee
    if typee == 'modificar_array':
        key = root.childs[0].typee
        lista = root.childs[1]
        p_list = []
        for node in lista.childs:
            v = eval_expression(node)
            p_list.append(v)
        schema = get_id(key) or {}
        original_schema = schema
        for i in range(0, len(p_list) - 1):
            elem = p_list[i]
            if schema.get(elem) is None:
                schema[elem] = {}
            schema = schema[elem]
        if schema is not None:
            ix = p_list[len(p_list) - 1]
            if isinstance(schema, str) and isinstance(ix, int):
                s = list(schema)
                while len(s) <= ix:
                    s.append('')
                s[ix] = value

                # reset
                schema = original_schema
                for i in range(0, len(p_list) - 2):
                    elem = p_list[i]
                    if schema.get(elem) is None:
                        schema[elem] = {}
                    schema = schema[elem]
                ix = p_list[len(p_list) - 2]
                schema[ix] = "".join(s)
            else:
                schema[ix] = value

        rsp = list(filter(lambda x: (x.key != key), globales.sym_table))
        globales.sym_table = rsp
        globales.sym_table.append(globales.SymTable(key, original_schema, 0, 0))
        return None

    return typee


def eval_assign(root: ASTNode):
    der = eval_expression(root.childs[1])
    izq = eval_modificar_array(root.childs[0], der)

    if izq:
        # Elimino el valor que estaba antes
        rsp = list(filter(lambda x: (x.key != izq), globales.sym_table))
        globales.sym_table = rsp
        globales.sym_table.append(globales.SymTable(izq, der, 0, 0))


def eval_control_statement(root: ASTNode):
    tag = root.childs[1].typee
    der = eval_expression(root.childs[0])
    return {'tag': tag, 'bool': der}


def run(root: ASTNode):
    global console_handler
    while root is not None:
        if root.nid == 521:
            print('..')
        if root.typee == 'declaracion_asignacion':
            eval_assign(root)
        if root.typee == 'unset':
            e_unset(root.childs[0].childs[0].typee)
        elif root.typee == 'sentencia_control':
            rsp = eval_control_statement(root)
            if rsp['bool']:
                root = globales.all_tags[rsp['tag']].next
                continue
        elif root.typee == 'salto_incondicional':
            tag = root.childs[0].typee
            root = globales.all_tags[tag].next
            continue
            pass
        elif root.typee == 'print':
            console_handler(str(eval_expression(root.childs[0])).replace("\\n", "\n"))
            pass
        elif root.typee == 'error':
            console_handler("Hubo un error en la gramatica")
            root = None
            continue
        elif root.typee == 'exit' or root.next is None:
            root = None
            continue

        root = root.next


def debug(root: ASTNode):
    global console_handler
    if root.nid == 521:
        print('..')
    if root.typee == 'declaracion_asignacion':
        eval_assign(root)
    if root.typee == 'unset':
        e_unset(root.childs[0].childs[0].typee)
    elif root.typee == 'sentencia_control':
        rsp = eval_control_statement(root)
        if rsp['bool']:
            return globales.all_tags[rsp['tag']].next
    elif root.typee == 'salto_incondicional':
        tag = root.childs[0].typee
        return globales.all_tags[tag].next
    elif root.typee == 'print':
        console_handler(str(eval_expression(root.childs[0])).replace("\\n", "\n"))
    elif root.typee == 'error':
        console_handler("Hubo un error en la gramatica")

    return root.next
