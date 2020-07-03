from __future__ import annotations
from ply.lex import Lexer
from enum import Enum
from typing import List, Optional
from compi.gramaticas.globales import all_tags

nid = 0
eti = {"init"}


class ASTTypes:
    EXPRESSION = "expression"
    NUM = "num"
    print = 'print'
    etiqueta = 'etiqueta'
    expresion_number = 'expresion_number'
    end = 'end'
    sentencia_control = 'sentencia_control'
    salto_incondicional = 'salto_incondicional'
    declaracion_asignacion = 'declaracion_asignacion'


class ASTNode:
    def __init__(self, typee: str, line: int = 0, col: int = 0, value=None, *args):
        global nid, eti
        eti.add(typee)
        self.typee = typee
        self.value = value
        self.line = line
        self.col = col
        self.childs: List[ASTNode] = list(args or [])
        self.next = None

        nid = nid + 1
        self.nid = nid

    def add_child(self, c: ASTNode):
        self.childs.append(c)

    def genarar_lista(self):
        for i in range(0, len(self.childs) - 1):
            self.childs[i].next = self.childs[i + 1]

            if self.childs[i].typee == ASTTypes.etiqueta and all_tags.get(self.childs[i].childs[0].typee) is None:
                all_tags[self.childs[i].childs[0].typee] = self.childs[i]

        return self.childs[0]

    def write_node(self):
        string = [
            '\tnode{nid} [label="[{nid}]\\n{label}"]'.format(
                nid=str(self.nid), label="{}\\n{}".format(self.typee, str(self.value or ""))
            )
        ]
        for c in self.childs:
            string.append(c.write_node())
            string.append(
                "\tnode{nid} -> node{cnid}".format(nid=str(self.nid), cnid=c.nid)
            )

        return "\n".join(string)

    def to_str(self):
        return """digraph ASTNode {{\n{c}\n}}""".format(c=self.write_node())

    def __repr__(self):
        return "[{}]{}".format(self.nid, self.typee)


class LexToken:
    def __init__(self):
        self.lineno = None
        self.value = None
        self.type = None
        self.lexpos = None
        self.lexer: Optional[Lexer] = None

    def __str__(self):
        return 'LexToken(%s,%r,%d,%d)' % (self.type, self.value, self.lineno, self.lexpos)

    def __repr__(self):
        return str(self)
