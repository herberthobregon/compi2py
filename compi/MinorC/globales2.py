from typing import List


def guardar_etiqueta(pa: str):
    global etiquetilla
    etiquetilla = pa


class SymTable:
    def __init__(self, key: str, value: any, line: int = 0, col: int = 0):
        self.key = key
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return "{{key:{}, value:{}}}".format(self.key, self.value)


class CError:
    def __init__(self, descrip: str, line: int, col: int, t: str):
        self.decrip = descrip
        self.line = line
        self.col = col
        self.t = t

    def __repr__(self):
        return "{}, {}:{} {}".format(self.t, self.line, self.col, self.decrip)


entrada = ""
etiquetilla = ""
lEtiquetasAmbito = {}

lErrores: List[CError] = []
lErroresSemanticos: List[CError] = []
all_tags = {}
sym_table: List[SymTable] = []
sym_table_fun: List[SymTable] = []
lGramaticaUsada = []

indice = 0
r_shiftreduce_grammar = []


def restart_all():
    global lEtiquetasAmbito,sym_table_fun, lErrores, lErroresSemanticos, all_tags, sym_table, lGramaticaUsada, indice, r_shiftreduce_grammar
    lEtiquetasAmbito = {}
    lErrores = []
    lErroresSemanticos = []
    all_tags = {}
    sym_table = []
    sym_table_fun = []
    lGramaticaUsada = []
    indice = 0
    r_shiftreduce_grammar = []
