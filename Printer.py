from ParseTree import Procedure, DeclSeq, Decl, StmtSeq, Assign, Print, Read, Expr, Term, Factor, If, Loop, Cond, Cmpr
class Printer:
    def print_procedure(self, procedure):
        print(f"procedure {procedure.name} is")

        if procedure.decl_seq is not None:
            self.print_decl_seq(procedure.decl_seq, 0)

        print("begin")
        self.print_stmt_seq(procedure.stmt_seq, 1)
        print("end")

    def print_decl_seq(self, decl_seq, indent):
        for decl in decl_seq.decls:
            self.print_decl(decl, indent)

    def print_decl(self, decl, indent):
        self.write_indent(indent)
        print(f"{decl.var_type} {decl.name};")

    def print_stmt_seq(self, stmt_seq, indent):
        for stmt in stmt_seq.stmts:
            self.print_stmt(stmt, indent)

    def print_stmt(self, stmt, indent):
        if isinstance(stmt, Decl):
            self.print_decl(stmt, indent)
        elif isinstance(stmt, Assign):
            self.print_assign(stmt, indent)
        elif isinstance(stmt, Print):
            self.print_print(stmt, indent)
        elif isinstance(stmt, Read):
            self.print_read(stmt, indent)
        elif isinstance(stmt, If):
            self.print_if(stmt, indent)
        elif isinstance(stmt, Loop):
            self.print_loop(stmt, indent)
        else:
            raise Exception(f"ERROR: Unknown statement type in printer")
        
    def print_assign(self, assign, indent):
        self.write_indent(indent)

        if assign.kind == "normal":
            print(f"{assign.name1} = {self.expr_to_string(assign.expr)};")

        elif assign.kind == "object_index":
            print(f"{assign.name1}['{assign.string}'] = {self.expr_to_string(assign.expr)};")

        elif assign.kind == "new_object":
            print(f"{assign.name1} = new object('{assign.string}', {self.expr_to_string(assign.expr)});")

        elif assign.kind == "colon":
            print(f"{assign.name1} : {assign.name2};")

        else:
            raise Exception(f"ERROR: Unknown assignment type in printer")
        
    def print_print(self, print_stmt, indent):
        self.write_indent(indent)
        print(f"print({self.expr_to_string(print_stmt.expr)});")

    def print_read(self, read_stmt, indent):
        self.write_indent(indent)
        print(f"read({read_stmt.name});")

    def print_if(self, if_stmt, indent):
        self.write_indent(indent)
        print(f"if {self.cond_to_string(if_stmt.cond)} then")

        self.print_stmt_seq(if_stmt.then_seq, indent + 1)

        if if_stmt.else_seq is not None:
            self.write_indent(indent)
            print("else")
            self.print_stmt_seq(if_stmt.else_seq, indent + 1)

        self.write_indent(indent)
        print("end")

    def print_loop(self, loop, indent):
        self.write_indent(indent)
        print(
            f"for ({loop.var_name} = {self.expr_to_string(loop.start_expr)}; "
            f"{self.cond_to_string(loop.cond)}; "
            f"{self.expr_to_string(loop.update_expr)}) do"
        )

        self.print_stmt_seq(loop.stmt_seq, indent + 1)

        self.write_indent(indent)
        print("end")

    def cond_to_string(self, cond):
        if cond.kind == "not":
            return f"not {self.cond_to_string(cond.cond)}"
        
        elif cond.kind == "bracket":
            return f"[{self.cond_to_string(cond.cond)}]"
        
        elif cond.kind == "cmpr":
            return self.cmpr_to_string(cond.left)
        
        elif cond.kind == "binary":
            return f"{self.cmpr_to_string(cond.left)} {cond.op} {self.cond_to_string(cond.right)}"
        
        raise Exception("ERROR: Unknown condiiton type type in printer")
    
    def cmpr_to_string(self, cmpr):
        return f"{self.expr_to_string(cmpr.left_expr)} {cmpr.op} {self.expr_to_string(cmpr.right_expr)}"

    def expr_to_string(self, expr):
        result = self.term_to_string(expr.term)

        if expr.op is not None:
            result += f" {expr.op} {self.expr_to_string(expr.expr)}"

        return result
    
    def term_to_string(self, term):
        result = self.factor_to_string(term.factor)

        if term.op is not None:
            result += f" {term.op} {self.term_to_string(term.term)}"

        return result
    
    def factor_to_string(self, factor):
        if factor.kind == "id":
            return factor.value
        
        elif factor.kind == "const":
            return str(factor.value)
        
        elif factor.kind == "object_index":
            return f"{factor.value}['{factor.string}']"
        
        elif factor.kind == "paren":
            return f"({self.expr_to_string(factor.expr)})"
        
        raise Exception("ERROR: Unknown factor type in printer")
    
    def write_indent(self, indent):
        print("    " * indent, end="")