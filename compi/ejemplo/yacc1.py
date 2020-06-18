
from compi.ejemplo.lex1 import tokens
from compi.helpers.ast import ASTNode, ASTTypes

precedence = (
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIV"),
    ("nonassoc", "UMINUS"),
)

def p_expr2uminus(p):
    "expr : MINUS expr %prec UMINUS"
    line   = p.lineno(0)
    col  = p.lexpos(0) 
    p[0] = ASTNode(ASTTypes.NUM.value, line, col, -p[2]) 

def p_expression_binop(p):
    """expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIV expr"""
    
    line   = p.lineno(0)        
    col  = p.lexpos(0)       
    if p[2] == "/":
        if p[3] == 0:
            print("Can't divide by 0")
            raise ZeroDivisionError("integer division by 0")

    p[0] = ASTNode(ASTTypes.EXPRESSION.value, line, col, p[2], p[1], p[3])


def p_expr2NUM(p):
    "expr : NUMBER"
    line   = p.lineno(0)
    col  = p.lexpos(0)  
    p[0] = ASTNode(ASTTypes.NUM.value, line, col, p[1])

def p_parens(p):
    "expr : LPAREN expr RPAREN"
    p[0] = p[2]


def p_error(p):
    print("Syntax error in input!")