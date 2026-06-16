from ParseTree import Decl, Assign, Print, Read, If, Loop

class Memory:
    def __init__(self):
        # Global variables
        self.global_vars = {}

        #Stack of local scopes for begin/end, if, else, and loop blocks
        self.local_scopes = []

    def push_scope(self):
        self.local_scopes.append({})

    def pop_scope(self):
        self.local_scopes.pop()

    def declare(self, decl, is_global=False):
        if decl.var_type == "integer":
            entry = {
                "type": "integer",
                "value": 0
            }
        else:
            entry = {
                "type": "object",
                "value": None
            }

        if is_global:
            self.global_vars[decl.name] = entry
        else:
            self.local_scopes[-1][decl.name] = entry

    def get_entry(self, name):
        for scope in reversed(self.local_scopes):
            if name in scope:
                return scope[name]
            
        if name in self.global_vars:
            return self.global_vars[name]
        
        raise Exception(f"ERROR: Variable '{name}' not found during execution")
    
    def get_value(self, name):
        entry = self.get_entry(name)

        if entry["type"] == "integer":
            return entry["value"]
        
        obj = entry["value"]

        if obj is None:
            raise Exception(f"ERROR: Object variable '{name}' is null")
        
        default_key = obj["default_key"]

        if default_key not in obj["values"]:
            raise Exception(f"ERROR: Default key missing for object '{name}'")
        
        return obj["values"][default_key]
    
    def set_value(self, name, value):
        entry = self.get_entry(name)

        if entry["type"] == "integer":
            entry["value"] = value
            return
        
        obj = entry["value"]

        if obj is None:
            raise Exception(f"ERROR: Object variable '{name}' is null")
        
        default_key = obj["default_key"]
        obj["values"][default_key] = value

    def new_object(self, name, default_key, value):
        entry = self.get_entry(name)

        if entry["type"] != "object":
            raise Exception(f"Error: Variable '{name}' is not object")
        
        entry["value"] = {
            "default_key": default_key,
            "values": {
                default_key: value
            }
        }

    def set_object_key(self, name, key, value):
        entry = self.get_entry(name)

        if entry["type"] != "object":
            raise Exception(f"ERROR: Object variable '{name}' is not object")
        
        obj = entry["value"]

        if obj is None:
            raise Exception(f"ERROR: Object variable '{name}' is null")

        obj["values"][key] = value

    def get_object_key(self, name, key):
        entry = self.get_entry(name)

        if entry["type"] != "object":
            raise Exception(f"ERROR: Variable '{name}' is not object")

        obj = entry["value"]

        if obj is None:
            raise Exception(f"ERROR: Object variable '{name}' is null")

        if key not in obj["values"]:
            raise Exception(f"ERROR: Key '{key}' not found in object '{name}'")

        return obj["values"][key]

    def assign_reference(self, left_name, right_name):
        left_entry = self.get_entry(left_name)
        right_entry = self.get_entry(right_name)

        if left_entry["type"] != "object" or right_entry["type"] != "object":
            raise Exception("ERROR: Reference assignment requires object variables")

        if right_entry["value"] is None:
            raise Exception(f"ERROR: Object variable '{right_name}' is null")

        left_entry["value"] = right_entry["value"]


class DataReader:
    def __init__(self, data_file):
        try:
            with open(data_file, "r") as f:
                text = f.read().strip()
        except FileNotFoundError:
            raise Exception(f"ERROR: Data file '{data_file}' not found")

        if text == "":
            self.values = []
        else:
            self.values = [int(value) for value in text.split()]

        self.index = 0

    def read_next(self):
        if self.index >= len(self.values):
            raise Exception("ERROR: Not enough data values for read")

        value = self.values[self.index]
        self.index += 1
        return value


class Executor:
    def __init__(self, data_file):
        self.memory = Memory()
        self.data_reader = DataReader(data_file)

    def execute_procedure(self, procedure):
        # Execute global declarations before begin
        if procedure.decl_seq is not None:
            for decl in procedure.decl_seq.decls:
                self.memory.declare(decl, is_global=True)

        # Main begin/end block gets a local scope
        self.memory.push_scope()
        self.execute_stmt_seq(procedure.stmt_seq)
        self.memory.pop_scope()

    def execute_stmt_seq(self, stmt_seq):
        for stmt in stmt_seq.stmts:
            self.execute_stmt(stmt)

    def execute_stmt(self, stmt):
        if isinstance(stmt, Decl):
            self.memory.declare(stmt, is_global=False)

        elif isinstance(stmt, Assign):
            self.execute_assign(stmt)

        elif isinstance(stmt, Print):
            value = self.eval_expr(stmt.expr)
            print(value)

        elif isinstance(stmt, Read):
            value = self.data_reader.read_next()
            self.memory.set_value(stmt.name, value)

        elif isinstance(stmt, If):
            if self.eval_cond(stmt.cond):
                self.memory.push_scope()
                self.execute_stmt_seq(stmt.then_seq)
                self.memory.pop_scope()
            elif stmt.else_seq is not None:
                self.memory.push_scope()
                self.execute_stmt_seq(stmt.else_seq)
                self.memory.pop_scope()

        elif isinstance(stmt, Loop):
            self.memory.set_value(stmt.var_name, self.eval_expr(stmt.start_expr))

            while self.eval_cond(stmt.cond):
                self.memory.push_scope()
                self.execute_stmt_seq(stmt.stmt_seq)
                self.memory.pop_scope()

                self.memory.set_value(stmt.var_name, self.eval_expr(stmt.update_expr))

        else:
            raise Exception("ERROR: Unknown statement during execution")

    def execute_assign(self, assign):
        if assign.kind == "normal":
            value = self.eval_expr(assign.expr)
            self.memory.set_value(assign.name1, value)

        elif assign.kind == "new_object":
            value = self.eval_expr(assign.expr)
            self.memory.new_object(assign.name1, assign.string, value)

        elif assign.kind == "object_index":
            value = self.eval_expr(assign.expr)
            self.memory.set_object_key(assign.name1, assign.string, value)

        elif assign.kind == "colon":
            self.memory.assign_reference(assign.name1, assign.name2)

        else:
            raise Exception("ERROR: Unknown assignment kind during execution")

    def eval_cond(self, cond):
        if cond.kind == "not":
            return not self.eval_cond(cond.cond)

        elif cond.kind == "bracket":
            return self.eval_cond(cond.cond)

        elif cond.kind == "cmpr":
            return self.eval_cmpr(cond.left)

        elif cond.kind == "binary":
            left_value = self.eval_cmpr(cond.left)

            if cond.op == "or":
                return left_value or self.eval_cond(cond.right)

            elif cond.op == "and":
                return left_value and self.eval_cond(cond.right)

            else:
                raise Exception("ERROR: Unknown condition operator")

        else:
            raise Exception("ERROR: Unknown condition kind during execution")

    def eval_cmpr(self, cmpr):
        left = self.eval_expr(cmpr.left_expr)
        right = self.eval_expr(cmpr.right_expr)

        if cmpr.op == "==":
            return left == right

        elif cmpr.op == "<":
            return left < right

        else:
            raise Exception("ERROR: Unknown comparison operator")

    def eval_expr(self, expr):
        value = self.eval_term(expr.term)

        if expr.op == "+":
            return value + self.eval_expr(expr.expr)

        elif expr.op == "-":
            return value - self.eval_expr(expr.expr)

        return value

    def eval_term(self, term):
        value = self.eval_factor(term.factor)

        if term.op == "*":
            return value * self.eval_term(term.term)

        elif term.op == "/":
            divisor = self.eval_term(term.term)

            if divisor == 0:
                raise Exception("ERROR: Division by 0")

            return value // divisor

        return value

    def eval_factor(self, factor):
        if factor.kind == "id":
            return self.memory.get_value(factor.value)

        elif factor.kind == "const":
            return factor.value

        elif factor.kind == "object_index":
            return self.memory.get_object_key(factor.value, factor.string)

        elif factor.kind == "paren":
            return self.eval_expr(factor.expr)

        else:
            raise Exception("ERROR: Unknown factor during execution")