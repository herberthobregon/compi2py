import ply.lex
import ply.yacc
from graphviz import Source
from compi.helpers.ast import ASTNode
from compi.MinorC import lex2
from compi.MinorC import yacc2

from PyQt5 import QtWidgets, QtCore, QtGui
from typing import Optional, List
import re
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


def get_ast(txt: str, cnxx: any, console_handlerx: any) -> ASTNode:
    global cnx, console_handler
    console_handler = console_handlerx
    cnx = cnxx
    lexer = ply.lex.lex(module=lex2)
    globales2.entrada = txt
    parser = ply.yacc.yacc(module=yacc2, tabmodule="yacc2_tab", start='init')
    root: ASTNode = parser.parse(input=txt, lexer=lexer)  # the input

    dot = Source(root.to_str())
    dot.format = 'png'
    dot.render('graph')

    # lista = root.genarar_lista()
    # run(lista)
    # print("\n".join([str(i) for i in globales2.sym_table]))
    parser.restart()
    return root


# def debug_ast(txt: str, cnxx: any, console_handlerx: any) -> ASTNode:
#     global cnx, console_handler, next_ats
#     console_handler = console_handlerx
#     cnx = cnxx
#     lexer = ply.lex.lex(module=lex1)
#     parser = ply.yacc.yacc(module=yacc1, tabmodule="yacc1_tab")
#     root: ASTNode = parser.parse(txt)  # the input
#
#     dot = Source(root.to_str())
#     dot.format = 'png'
#     dot.render('graph')
#
#     lista = root.genarar_lista()
#     next_ats = debug(lista)
#     return next_ats


def step():
    global cnx, console_handler, next_ats
    next_ats = debug(next_ats)
    return next_ats


def run(root: ASTNode):
    global console_handler
    while root is not None:
        if root.nid == 521:
            print('..')
        root = root.next


def debug(root: ASTNode):
    global console_handler
    if root.nid == 521:
        print('..')

    return root.next
