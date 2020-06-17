from enum import Enum

nid = 0


class ASTTypes(Enum):
    EXPRESSION = "expression"
    NUM = "num"


class ASTNode:
    def __init__(self, label: ASTTypes, line: int, col: int, value: any, *args):
        global nid
        self.label = label
        self.value = value
        self.childs = args
        nid = nid + 1
        self.nid = nid
    
    def exe(self):
        return 0

    def write_node(self):
        string = [
            '\tnode{nid} [label="{label}"]'.format(
                nid=str(self.nid), label="{}\\n{}".format(self.label, str(self.value))
            )
        ]
        for c in self.childs:
            string.append(c.write_node())
            string.append(
                "\tnode{nid} -> node{cnid}".format(nid=str(self.nid), cnid=c.nid)
            )

        return "\n".join(string)

    def __repr__(self):
        return """digraph ASTNode {{\n{c}\n}}""".format(c=self.write_node())
