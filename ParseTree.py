class Procedure:
    def __init__(self, name, decl_seq, stmt_seq):
        self.name = name
        self.decl_seq = decl_seq
        self.stmt_seq = stmt_seq

class DeclSeq:
    def __init__(self, decls):
        self.decls = decls

class Decl:
    def __init__(self, var_type, name):
        self.var_type = var_type
        self.name = name

class StmtSeq:
    def __init__(self, stmts):
        self.stmts = stmts

class Assign:
    def __init__(self, kind, name1, expr=None, string=None, name2=None):
        self.kind = kind
        self.name1 = name1
        self.expr = expr
        self.string = string
        self.name2 = name2

class Print:
    def __init__(self, expr):
        self.expr = expr

class Read:
    def __init__(self, name):
        self.name = name

class Expr:
    def __init__(self, term, op=None, expr=None):
        self.term = term
        self.op = op
        self.expr = expr

class Term:
    def __init__(self, factor, op=None, term=None):
        self.factor = factor
        self.op = op
        self.term = term

class Factor:
    def __init__(self, kind, value=None, expr=None, string=None):
        self.kind = kind
        self.value = value
        self.expr = expr
        self.string = string

class If:
    def __init__(self, cond, then_seq, else_seq=None):
        self.cond = cond
        self.then_seq = then_seq
        self.else_seq = else_seq

class Loop:
    def __init__(self, var_name, start_eexpr, cond, update_expr, stmt_seq):
        self.var_name = var_name
        self.start_expr = start_eexpr
        self.cond = cond
        self.update_expr = update_expr
        self.stmt_seq = stmt_seq

class Cond:
    def __init__(self, kind, left=None, right=None, op=None, cond=None):
        self.kind = kind
        self.left = left
        self.right = right
        self.op = op
        self.cond = cond

class Cmpr:
    def __init__(self, left_expr, op, right_expr):
        self.left_expr = left_expr
        self.op = op
        self.right_expr = right_expr