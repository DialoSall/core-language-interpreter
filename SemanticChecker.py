from ParseTree import Decl, Assign, Print, Read, If, Loop


class SemanticChecker:
    def check(self, parse_tree):
        # scopes is a stack of dictionaries.
        # each dictionary maps variable name -> type.
        scopes = []

        # Global scope for declarations before begin
        scopes.append({})

        if parse_tree.decl_seq is not None:
            for decl in parse_tree.decl_seq.decls:
                self.declare(decl, scopes)

        # Local scope for the main begin/end block
        scopes.append({})
        self.check_stmt_seq(parse_tree.stmt_seq, scopes)
        scopes.pop()

    def declare(self, decl, scopes):
        current_scope = scopes[-1]

        if decl.name in current_scope:
            raise Exception(f"ERROR: Variable '{decl.name}' declared twice in same scope")
        
        current_scope[decl.name] = decl.var_type

    def lookup(self, name, scopes):
        # Search from innermost scope outward
        for scope in reversed(scopes):
            if name in scope:
                return scope[name]
            
        raise Exception(f"ERROR: Variable '{name}' used before declaration")
    
    def require_object(self, name, scopes):
        var_type = self.lookup(name, scopes)

        if var_type != "object":
            raise Exception(f"ERROR: Variable '{name}' must be object")
        
    def check_stmt_seq(self, stmt_seq, scopes):
        for stmt in stmt_seq.stmts:
            self.check_stmt(stmt, scopes)
    
    def check_stmt(self, stmt, scopes):
        if isinstance(stmt, Decl):
            self.declare(stmt, scopes)

        elif isinstance(stmt, Assign):
            self.check_assign(stmt, scopes)

        elif isinstance(stmt, Print):
            self.check_expr(stmt.expr, scopes)

        elif isinstance(stmt, Read):
            self.lookup(stmt.name, scopes)

        elif isinstance(stmt, If):
            self.check_cond(stmt.cond, scopes)

            # New local scope for then branch
            scopes.append({})
            self.check_stmt_seq(stmt.then_seq, scopes)
            scopes.pop()

            # New local scope for else branch
            if stmt.else_seq is not None:
                scopes.append({})
                self.check_stmt_seq(stmt.else_seq, scopes)
                scopes.pop()

        elif isinstance(stmt, Loop):
            self.lookup(stmt.var_name, scopes)
            self.check_expr(stmt.start_expr, scopes)
            self.check_cond(stmt.cond, scopes)
            self.check_expr(stmt.update_expr, scopes)

            # New local scope for loop body
            scopes.append({})
            self.check_stmt_seq(stmt.stmt_seq, scopes)
            scopes.pop()

        else:
            raise Exception("ERROR: Unknown statement type in semantic checker")
    
    def check_assign(self, assign, scopes):
        # Make sure left-hand variable exists
        self.lookup(assign.name1, scopes)

        if assign.kind == "normal":
            self.check_expr(assign.expr, scopes)

        elif assign.kind == "new_object":
            # id = new object(string, expr);
            # id must be object
            self.require_object(assign.name1, scopes)
            self.check_expr(assign.expr, scopes)

        elif assign.kind == "object_index":
            # id[string] = expr;
            # id must be object
            self.require_object(assign.name1, scopes)
            self.check_expr(assign.expr, scopes)

        elif assign.kind == "colon":
            # id : id;
            # both must be object
            self.require_object(assign.name1, scopes)
            self.require_object(assign.name2, scopes)

        else:
            raise Exception("ERROR: Unknown assignment type in semantic checker")

    def check_cond(self, cond, scopes):
        if cond.kind == "not":
            self.check_cond(cond.cond, scopes)

        elif cond.kind == "bracket":
            self.check_cond(cond.cond, scopes)

        elif cond.kind == "cmpr":
            self.check_cmpr(cond.left, scopes)

        elif cond.kind == "binary":
            self.check_cmpr(cond.left, scopes)
            self.check_cond(cond.right, scopes)

        else:
            raise Exception("ERROR: Unknown condition type in semantic checker")

    def check_cmpr(self, cmpr, scopes):
        self.check_expr(cmpr.left_expr, scopes)
        self.check_expr(cmpr.right_expr, scopes)

    def check_expr(self, expr, scopes):
        self.check_term(expr.term, scopes)

        if expr.expr is not None:
            self.check_expr(expr.expr, scopes)

    def check_term(self, term, scopes):
        self.check_factor(term.factor, scopes)

        if term.term is not None:
            self.check_term(term.term, scopes)

    def check_factor(self, factor, scopes):
        if factor.kind == "id":
            self.lookup(factor.value, scopes)

        elif factor.kind == "const":
            return

        elif factor.kind == "object_index":
            # id[string] used as a factor
            # id must be declared and must be object
            self.require_object(factor.value, scopes)

        elif factor.kind == "paren":
            self.check_expr(factor.expr, scopes)

        else:
            raise Exception("ERROR: Unknown factor type in semantic checker")
