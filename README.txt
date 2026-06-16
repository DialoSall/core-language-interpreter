Dialo Sall

CSE 3341 Project 3 = CORE Interpreter

Submitted Files:

Core.py
Contains the Core token enum used by the scanner and parser.

Scanner.py
Contains the lexical analyzer from Project 1. It reads the input .code file and
produces Core tokens for the parser.

Parser.py
Contains the recursive descent parser for the Core grammar. It reads the tokens from
the scanner and builds a parse tree for the input program.

ParseTree.py
Contains the classes used to represent the parse tree. These classes include
Procedure, DeclSeq. Decl, StmtSeq, Assign, Print, Read, If, Loop, Cond, Cmpr, Expr,
Term, and Factor.

SemnaticChecker.py
Contains the semantic checking logic from project 2. It checks that variables are
declared before use, variables are not declared twice in the same scope, and object
variables are used correctly in object operations.

Executor.py
Contains the interpretor/executor for Project 3. It recursively walks the parse tree
and executes declarations, assignments, print statements, read statements, if
statements, loops, conditions, expressions, terms, and factors.

Main.py
Contains the main procedure for the project. It takes a .code file and a .data file
from the command line, creates the scanner, parses the program, performs semantic checks,
and then executes the program.

README.txt
Contains the description of the submitted files, design, testing, and known bugs.

Comments/Special Features:
Building off of project 2, project 3 executes the parse tree using a separate file
instead of printing the program. There aren't really any special features with how 
I approached this, more or less a head-on approach.

Overall Design:

The program begins in Main.py where it expects a .code file and a .data file as input
for the Core Program and read statements respectively. Main.py then creates a scanner
for the .code file, passes it to the Parser, builds a parse tree, runs the SemanticChecker,
and then creates an executor to execute the parse tree.

The executor uses recursive descent over the parse tree. Each major parse tree structure
has a corresponding execution/evaluation function. Each node type has a function like 
"execute_stmt" or "eval_factor". Condition nodes return boolean values and expression nodes
return integer values.

Variable and Memory Design:

Memory is handled using a Memory class inside Executor.py. Global variables are stored
in a dictionary called global_vars. Local variables are stored using a stack of dictionaries
called local_scopes. When the executor enters a new local block, such as the main begin/end
block, an if branch, else branch, or loop body, it pushes a new local scope. When execution 
leaves that block, the local scope is popped. Variable lookup searches from the innermost local
scope outward, then checks the global scope. (this is basically how we discussed the process
in class.)

Integer variables use the value model. When an integer is declared, it starts with value 0.

Object variables use the reference model. When an object is declared, it starts as null. A new
object assignment creates a dictionary-like oboject with a default key and integer value. Object
lookup thorugh id['string'] retrieves the value for a specific key. Using an object variable without
brackets accesses its default key. The colon assignment makes two object variables refer to the same 
object.

Runtime Error Handling:

The executor checks for the required runtime errors. If a read statement executes after all values in
the .data file have already been used, the program prints an error message. If division by 0 is attempted,
the program prints an error message. If an object key is accessed but the key does not exist, the program 
prints an error message. The executor also reports null object usage when an object operation is 
attempted on an object variable that does not refer to an object.

Testing:

I tested the interpreter using the provided tester.sh script with the Correct and Error test folders. 
All 30 correct test cases passed by matching the expected output. All 4 provided runtime error cases 
also produced related error messages. I also manually tested small programs involving read, print, arithmetic expressions,
if statements, for loops, object creation, object key assignment, object lookup, and object reference assignment.
I have not detecting any remaining bugs.