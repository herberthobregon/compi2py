from ply import lex

import ply.yacc as yacc
from py.lang_def import lex1, yacc1

lexer = lex.lex(module=lex1)
parser = yacc.yacc(module=yacc1, tabmodule="yacc1_tab")

root = parser.parse("1+2*9+(3*2)+1")  # the input
print(root)
