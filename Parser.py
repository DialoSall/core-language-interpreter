from Core import Core
from ParseTree import Procedure, DeclSeq, Decl, StmtSeq, Assign, Print, Read, Expr, Term, Factor, If, Loop, Cond, Cmpr, Function, Call


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner

    def current(self):
        return self.scanner.currentToken()
    
    def match(self, expected):
        if self.current() != expected:
            raise Exception(f"ERROR: Expected {expected.name}, found {self.current().name}")
        self.scanner.nextToken()

    def parse_procedure(self):
        # <procedure ::= procedure ID is <decl-seq> begin <stmt-seq> end
        #              | procedure ID is begin <stmt-seq> end>

        self.match(Core.PROCEDURE)

        if self.current() != Core.ID:
            raise Exception(f"ERROR: Expected procedure name")
        
        name = self.scanner.getID()
        self.match(Core.ID)

        self.match(Core.IS)

        decl_seq = None

        if self.current() in [Core.INTEGER, Core.OBJECT, Core.PROCEDURE]:
            decl_seq = self.parse_decl_seq()

        self.match(Core.BEGIN)

        stmt_seq = self.parse_stmt_seq()

        self.match(Core.END)

        if self.current() != Core.EOS:
            raise Exception(f"ERROR: Extra tokens after end")
        
        return Procedure(name, decl_seq, stmt_seq)
    
    def parse_decl_seq(self):
        decls = []

        while self.current() in [Core.INTEGER, Core.OBJECT, Core.PROCEDURE]:
            if self.current() == Core.PROCEDURE:
                decls.append(self.parse_function())
            else:
                decls.append(self.parse_decl())

        return DeclSeq(decls)
    
    def parse_function(self):
        self.match(Core.PROCEDURE)

        if self.current() != Core.ID:
            raise Exception("ERROR: Expected procedure name")
        
        name = self.scanner.getID()
        self.match(Core.ID)

        self.match(Core.LPAREN)
        self.match(Core.OBJECT)

        params = self.parse_parameters()

        if(len(params) != len(set(params))):
            raise Exception("ERROR: Duplicate formal parameter")
        
        self.match(Core.RPAREN)
        self.match(Core.IS)

        stmt_seq = self.parse_stmt_seq()

        self.match(Core.END)

        return Function(name, params, stmt_seq)
    
    def parse_parameters(self):
        params = []

        if self.current() != Core.ID:
            raise Exception("ERROR: Expected parameter name")
        
        params.append(self.scanner.getID())
        self.match(Core.ID)

        while self.current() == Core.COMMA:
            self.match(Core.COMMA)

            if self.current() != Core.ID:
                raise Exception("ERROR: Expected parameter name")
            
            params.append(self.scanner.getID())
            self.match(Core.ID)

        return params

    def parse_decl(self):
        if self.current() == Core.INTEGER:
            var_type = "integer"
            self.match(Core.INTEGER)
        elif self.current() == Core.OBJECT:
            var_type = "object"
            self.match(Core.OBJECT)
        else:
            raise Exception(f"ERROR: Expected declaration type")
        
        if self.current() != Core.ID:
            raise Exception(f"ERROR: Expected variable name in declaration")
        
        name = self.scanner.getID()
        self.match(Core.ID)

        self.match(Core.SEMICOLON)

        return Decl(var_type, name)
    
    def parse_stmt_seq(self):
        stmts = []

        while self.current() in [
            Core.ID,
            Core.IF,
            Core.FOR,
            Core.PRINT,
            Core.READ,
            Core.INTEGER,
            Core.OBJECT,
            Core.BEGIN
        ]:
            stmts.append(self.parse_stmt())

        if len(stmts) == 0:
            raise Exception("ERROR: Expected statement")
        
        return StmtSeq(stmts)
    
    def parse_stmt(self):
        if self.current() in [Core.INTEGER, Core.OBJECT]:
            return self.parse_decl()
        elif self.current() == Core.ID:
            return self.parse_assign()
        elif self.current() == Core.IF:
            return self.parse_if()
        elif self.current() == Core.FOR:
            return self.parse_loop()
        elif self.current() == Core.PRINT:
            return self.parse_print()
        elif self.current() == Core.READ:
            return self.parse_read()
        elif self.current() == Core.BEGIN:
            return self.parse_call()

        raise Exception("ERROR: invalid statement")
    
    def parse_call(self):
        self.match(Core.BEGIN)

        if self.current() != Core.ID:
            raise Exception("ERROR: Expected procedure name in call")
        
        name = self.scanner.getID()
        self.match(Core.ID)

        self.match(Core.LPAREN)

        args = self.parse_parameters()

        self.match(Core.RPAREN)
        self.match(Core.SEMICOLON)

        return Call(name, args)
    
    def parse_assign(self):
        if self.current() != Core.ID:
            raise Exception("ERROR: Expected assignment variable")
        
        name1 = self.scanner.getID()
        self.match(Core.ID)

        # id = ...
        if self.current() == Core.ASSIGN:
            self.match(Core.ASSIGN)
            
            #id = new object(string, <expr>);
            if self.current() == Core.NEW:
                self.match(Core.NEW)
                self.match(Core.OBJECT)
                self.match(Core.LPAREN)

                if self.current() != Core.STRING:
                    raise Exception("ERROR: Expected string in new object")
                
                string = self.scanner.getString()
                self.match(Core.STRING)

                self.match(Core.COMMA)
                expr = self.parse_expr()
                self.match(Core.RPAREN)
                self.match(Core.SEMICOLON)

                return Assign("new_object", name1, expr=expr, string=string)
            
            # id = <expr>;
            else:
                expr = self.parse_expr()
                self.match(Core.SEMICOLON)
                return Assign("normal", name1, expr=expr)
        
        # id[string] = <expr>;
        elif self.current() == Core.LSQUARE:
            self.match(Core.LSQUARE)

            if self.current() != Core.STRING:
                raise Exception("ERROR: Expected string index")
            
            string = self.scanner.getString()
            self.match(Core.STRING)
            self.match(Core.RSQUARE)
            self.match(Core.ASSIGN)

            expr = self.parse_expr()
            self.match(Core.SEMICOLON)

            return Assign("object_index", name1, expr=expr, string=string)
        
        # id : id;
        elif self.current() == Core.COLON:
            self.match(Core.COLON)

            if self.current() != Core.ID:
                raise Exception("ERROR: Expected object variable after colon")
            
            name2 = self.scanner.getID()
            self.match(Core.ID)
            self.match(Core.SEMICOLON)

            return Assign("colon", name1, name2=name2)
        
        else:
            raise Exception("ERROR: Invalid assignment")
        
    def parse_print(self):
        self.match(Core.PRINT)
        self.match(Core.LPAREN)
        expr = self.parse_expr()
        self.match(Core.RPAREN)
        self.match(Core.SEMICOLON)

        return Print(expr)
    
    def parse_read(self):
        self.match(Core.READ)
        self.match(Core.LPAREN)

        if self.current() != Core.ID:
            raise Exception("ERROR: Expected variable in read")
        
        name = self.scanner.getID()
        self.match(Core.ID)

        self.match(Core.RPAREN)
        self.match(Core.SEMICOLON)

        return Read(name)
    
    def parse_expr(self):
        term = self.parse_term()

        if self.current() == Core.ADD:
            self.match(Core.ADD)
            expr = self.parse_expr()
            return Expr(term, "+", expr)
        
        elif self.current() == Core.SUBTRACT:
            self.match(Core.SUBTRACT)
            expr = self.parse_expr()
            return Expr(term, "-", expr)
        
        return Expr(term)
    
    def parse_term(self):
        factor = self.parse_factor()

        if self.current() == Core.MULTIPLY:
            self.match(Core.MULTIPLY)
            term = self.parse_term()
            return Term(factor, "*", term)
        
        elif self.current() == Core.DIVIDE:
            self.match(Core.DIVIDE)
            term = self.parse_term()
            return Term(factor, "/", term)
        
        return Term(factor)
    
    def parse_factor(self):
        #id or id[string]
        if self.current() == Core.ID:
            name = self.scanner.getID()
            self.match(Core.ID)

            if self.current() == Core.LSQUARE:
                self.match(Core.LSQUARE)

                if self.current() != Core.STRING:
                    raise Exception("ERROR: Expected string index")
                
                string = self.scanner.getString()
                self.match(Core.STRING)
                self.match(Core.RSQUARE)

                return Factor("object_index", value=name, string=string)
            
            return Factor("id", value=name)
        
        # const
        elif self.current() == Core.CONST:
            value = self.scanner.getCONST()
            self.match(Core.CONST)
            return Factor("const", value=value)
        
        # ( <expr> )
        elif self.current() == Core.LPAREN:
            self.match(Core.LPAREN)
            expr = self.parse_expr()
            self.match(Core.RPAREN)
            return Factor("paren", expr=expr)
        
        else:
            raise Exception("ERROR: Invalid factor")
        
    def parse_if(self):
        self.match(Core.IF)

        cond = self.parse_cond()

        self.match(Core.THEN)

        then_seq = self.parse_stmt_seq()

        else_seq = None

        if self.current() == Core.ELSE:
            self.match(Core.ELSE)
            else_seq = self.parse_stmt_seq()
        
        self.match(Core.END)

        return If(cond, then_seq, else_seq)
    
    def parse_loop(self):
        self.match(Core.FOR)
        self.match(Core.LPAREN)

        if self.current() != Core.ID:
            raise Exception("ERROR: Expected loop variable")
        
        var_name = self.scanner.getID()
        self.match(Core.ID)

        self.match(Core.ASSIGN)

        start_expr = self.parse_expr()

        self.match(Core.SEMICOLON)

        cond = self.parse_cond()

        self.match(Core.SEMICOLON)

        update_expr = self.parse_expr()

        self.match(Core.RPAREN)

        self.match(Core.DO)

        stmt_seq = self.parse_stmt_seq()

        self.match(Core.END)

        return Loop(var_name, start_expr, cond, update_expr, stmt_seq)
    
    def parse_cond(self):
        # not <cond>
        if self.current() == Core.NOT:
            self.match(Core.NOT)
            cond = self.parse_cond()
            return Cond("not", cond=cond)
        
        # [ <cond> ]
        elif self.current() == Core.LSQUARE:
            self.match(Core.LSQUARE)
            cond = self.parse_cond()
            self.match(Core.RSQUARE)
            return Cond("bracket", cond=cond)
        
        # <cmpr>, <cmpr> or <cond>, <cmpr> and <cond>
        else:
            cmpr = self.parse_cmpr()

            if self.current() == Core.OR:
                self.match(Core.OR)
                cond = self.parse_cond()
                return Cond("binary", left=cmpr, op="or", right=cond)
            
            elif self.current() == Core.AND:
                self.match(Core.AND)
                cond = self.parse_cond()
                return Cond("binary", left=cmpr, op="and", right=cond)
            
            return Cond("cmpr", left=cmpr)
        
    def parse_cmpr(self):
        left_expr = self.parse_expr()

        if self.current() == Core.EQUAL:
            self.match(Core.EQUAL)
            right_expr = self.parse_expr()
            return Cmpr(left_expr, "==", right_expr)
        
        elif self.current() == Core.LESS:
            self.match(Core.LESS)
            right_expr = self.parse_expr()
            return Cmpr(left_expr, "<", right_expr)
        
        raise Exception("ERROR: Expected comparison operator")