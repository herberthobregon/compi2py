import ply.lex
import ply.yacc
from graphviz import Source
from compi.helpers.ast import ASTNode
from compi.MinorC import lex2
from compi.MinorC import yacc2

from PyQt5 import QtWidgets, QtCore, QtGui
from typing import Optional, List
from compi.MinorC import globales2

cnx: Optional[QtWidgets.QWidget] = None
console_handler: Optional[any] = None
next_ats: Optional[ASTNode] = None


def get_asta(txt: str, cnxx: any, console_handlerx: any) -> ASTNode:
    global cnx, console_handler
    console_handler = console_handlerx
    cnx = cnxx
    lexer = ply.lex.lex(module=lex2)
    globales2.entrada = txt
    lexer.input(txt)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)


def get_ast(txt: str, cnxx: any, console_handlerx: any):
    global cnx, console_handler
    globales2.restart_all()
    console_handler = console_handlerx
    cnx = cnxx
    lexer = ply.lex.lex(module=lex2)
    globales2.entrada = txt
    parser = ply.yacc.yacc(module=yacc2, tabmodule="yacc2_tab", start='init')
    root: ASTNode = parser.parse(input=txt, lexer=lexer)  # the input

    dot = Source(root.to_str())
    dot.format = 'svg'
    dot.render('report_minorc_graph')

    lista: List[ASTNode] = []
    for sentencias in root.childs[0]:
        for s in sentencias:
            lista.append(s)

    gen = Generator(lista)
    st = gen.get3d()
    # print("\n".join([str(i) for i in globales2.sym_table]))
    parser.restart()
    return st


def run(root: ASTNode):
    global console_handler
    while root is not None:
        if root.nid == 521:
            print('..')
        root = root.next


# ====================================================================================================

def evaluar_ast(ast: ASTNode):
    ast.code = ''
    value = ast.typee
    if isinstance(value, float) or isinstance(value, int):
        ast.value = ast.typee
        return ast
    elif isinstance(value, str):
        ast.value = "'{}'".format(ast.typee)
        return ast
    return 0


id_t = 0
# agumentos
id_a = 0
# retornos
id_v = 0


def gen_temp():
    global id_t
    id_t += 1
    resultado = "$t" + str(id_t)
    return resultado


def find_var(*args):
    key = "_".join(args)
    rsp = list(filter(lambda x: (x.key == key), globales2.sym_table))
    if len(rsp) > 0:
        return rsp[0].value
    else:
        return 0


def gen_id_temporal(value, *args):
    key = "_".join(args)
    rsp = list(filter(lambda x: (x.key == key), globales2.sym_table))
    if len(rsp) > 0:
        return rsp[0].value
    else:
        globales2.sym_table.append(globales2.SymTable(key, value))
        return key


def eval_expression(root: ASTNode, cnx=None):
    typee = root.typee
    exp_val = None

    if typee == '+' or typee == '-' \
            or typee == '*' \
            or typee == '/' \
            or typee == '%' \
            or typee == '&&' \
            or typee == '||' \
            or typee == 'xor' \
            or typee == '<' \
            or typee == '>' \
            or typee == '<=' \
            or typee == '>=' \
            or typee == '==' \
            or typee == '!=' \
            or typee == '&' \
            or typee == '|' \
            or typee == '^' \
            or typee == '<<' \
            or typee == '>>' \
            or typee == 'abs':
        exp_val = eval_plus(root, cnx)
    elif typee == 'expresion_number':
        data = root.childs[0].typee
        if data == 'access_arrayexp':
            exp_val = eval_expression(root.childs[0])
        # elif data == 'casteos':
        #     exp_val = cast_value(root.childs)
        elif data == 'array':
            exp_val = {}
        else:
            exp_val = evaluar_ast(root.childs[0])
    elif typee == 'expresion_id':
        data = root.childs[0]
        data.code = ''
        data.value = find_var(cnx, data.typee)
        exp_val = data
    elif typee == 'aum_dec':
        data = root.childs[0].childs[0]
        syym = root.childs[1].typee[:1]
        w_t = find_var(cnx, data.typee)
        data.code = '$t{nid} = {w_t};\n{w_t} = {w_t} {sym} 1;'.format(nid=root.nid, w_t=w_t, sym=syym)
        data.value = "$t{}".format(root.nid)
        exp_val = data

    if 'expresion_callfuncion' == typee:
        if root.childs[0].childs[0].typee == 'scanf':
            root.code = ''
            root.value = 'read()'
            exp_val = root
    # elif typee == 'access_arrayexp':
    #     key = root.childs[0].typee
    #     lista = root.childs[1]
    #     p_list = []
    #     for node in lista.childs:
    #         v = eval_expression(node)
    #         p_list.append(v)
    #     schema = get_id(key) or {}
    #     for i in range(0, len(p_list) - 1):
    #         elem = p_list[i]
    #         if schema.get(elem) is None:
    #             schema[elem] = {}
    #         schema = schema[elem]
    #     if schema is not None:
    #         exp_val = schema[p_list[len(p_list) - 1]]
    # elif typee == 'expresion_unaria':
    #     exp_val = eval_unaria(root.childs)
    # elif typee == 'exp_agrupacion':
    #     exp_val = eval_expression(root.childs[0])

    return exp_val


def eval_plus(root: ASTNode, cnx=None) -> ASTNode:
    childs: List[ASTNode] = root.childs
    prev_code_l = ''
    prev_code_r = ''
    if childs[0].value:
        prev_code_l = childs[0].code
        izq = childs[0].value
    else:
        r = eval_expression(childs[0], cnx)
        if isinstance(r, ASTNode):
            prev_code_l = r.code
            izq = r.value
        else:
            izq = r

    if childs[1].value:
        prev_code_r = childs[0].code
        der = childs[1].value
    else:
        r = eval_expression(childs[1], cnx)
        if isinstance(r, ASTNode):
            prev_code_r = r.code
            der = r.value
        else:
            der = r

    root.code = "{}{}$t{} = {} {} {};\n".format(prev_code_l, prev_code_r, str(root.nid), izq, root.typee, der)
    root.value = "$t{}".format(str(root.nid))

    return root


def eval_modificar_array(root: ASTNode, value: any):
    id_symtab = root.typee
    return id_symtab


def eval_assign(root: ASTNode, cnx=None):
    der = eval_expression(root, cnx)
    # Esto es por si solo viene int a = 1;
    if der and der.code == '':
        der.code = "$t{} = {};\n".format(str(root.nid), der.value)

    # key_symtab = eval_modificar_array(root.childs[0], der)
    # if key_symtab:
    #     # Elimino el valor que estaba antes
    #     rsp = list(filter(lambda x: (x.key != key_symtab), globales2.sym_table))
    #     globales2.sym_table = rsp
    #     globales2.sym_table.append(globales2.SymTable(key_symtab, der, 0, 0))
    return der


class GenFunctions:
    def __init__(self, node: ASTNode):
        node.code = ''
        node.value = None
        self.node = node
        self.name = node.childs[1].typee
        globales2.sym_table_fun.append(globales2.SymTable(self.name, node, node.line, node.col))
        for lista_instruc in node.childs[3]:
            if lista_instruc.typee == 'declaracion_registros':
                declaracion_registros = lista_instruc
                typee = declaracion_registros.childs[0].childs[0].typee  # int

                if 'tipo_declaracion2' == declaracion_registros.childs[1].childs[0].typee:
                    tipo_declaracion2 = declaracion_registros.childs[1].childs[0]

                    varname = tipo_declaracion2.childs[0].typee
                    root = eval_assign(tipo_declaracion2.childs[2], self.name)
                    uid = gen_id_temporal(root.value, self.name, varname)

                    prev = ''
                    if node.code:
                        prev = node.code

                    node.code = "{}{}\n".format(prev, root.code)

            if lista_instruc.typee == 'declaracion_structs':
                declaracion_registros = lista_instruc
                typee = declaracion_registros.childs[0].childs[0].typee  # int

                if 'tipo_declaracion2' == declaracion_registros.childs[1].childs[0].typee:
                    tipo_declaracion2 = declaracion_registros.childs[1].childs[0]

                    varname = tipo_declaracion2.childs[0].typee
                    root = eval_assign(tipo_declaracion2.childs[2], self.name)
                    uid = gen_id_temporal(root.value, self.name, varname)

                    prev = ''
                    if node.code:
                        prev = node.code

                    node.code = "{}{}\n".format(prev, root.code)

            if lista_instruc.typee == 'call_funcion':
                call_funcion = lista_instruc
                if 'printf' == call_funcion.childs[0].typee:
                    for exp in call_funcion.childs[1]:
                        root = eval_assign(exp, self.name)
                        prev = ''
                        if node.code:
                            prev = node.code

                        node.code = "{}{}{}\n".format(prev, root.code, 'print($t{});'.format(exp.nid))


            if lista_instruc.typee == 'sentencia_etiqueta':
                sentencia_etiqueta = lista_instruc
                tag = sentencia_etiqueta.childs[0].typee
                prev = ''
                if node.code:
                    prev = node.code
                node.code = "{}{}:\n".format(prev, tag)

    def to_str(self):
        return "{name}:\n{code}\n".format(name=self.name, code=self.node.code)


class Generator:
    def __init__(self, lista: List[ASTNode]):
        self.lista: List[GenFunctions] = []
        for node in lista:
            if node.typee == 'declaracion_funcion':
                g = GenFunctions(node)
                self.lista.append(g)

    def get3d(self):
        return '\n'.join([i.to_str() for i in self.lista])
