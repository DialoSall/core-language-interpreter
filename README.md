# CORE Language Interpreter

A Python interpreter for a custom imperative programming language. The project implements the full language-processing pipeline, including lexical analysis, recursive-descent parsing, semantic validation, scoped memory management, and program execution.

## Features

* Lexical analysis and tokenization
* Recursive-descent parsing
* Parse tree construction
* Semantic checking
* Global and nested local scopes
* Integer variables
* Object variables with reference semantics
* Object key-value storage
* Arithmetic expressions
* Conditional statements
* For loops
* Input from data files
* Runtime error handling

## Architecture

The interpreter is divided into several components:

* `Core.py` defines the language tokens.
* `Scanner.py` reads source code and converts it into tokens.
* `Parser.py` uses recursive descent to validate the grammar and build a parse tree.
* `ParseTree.py` defines the node classes used to represent programs.
* `SemanticChecker.py` validates declarations, scopes, and object usage.
* `Executor.py` manages memory and executes the parse tree.
* `Main.py` connects the scanner, parser, semantic checker, and executor.

## Memory Model

The interpreter models three forms of memory:

* Global memory for variables declared before the main program block
* Local memory using a stack of nested scopes
* Heap-style object storage using shared Python references

Integer variables use value semantics and are initialized to `0`.

Object variables use reference semantics and are initialized to `null`. Multiple object variables may refer to the same underlying object.

## Running the Interpreter

The interpreter accepts two command-line arguments:

1. A source-code file
2. A data file containing integer input values

```bash
python3 Main.py program.code program.data
```

Example:

```bash
python3 Main.py examples/sample.code examples/sample.data
```

Program output is printed to standard output.

## Runtime Error Handling

The interpreter detects and reports errors including:

* Insufficient input values
* Division by zero
* Accessing an undefined object key
* Using a null object reference
* Invalid variable or object operations

## Version History

### Version 1: Lexical Analyzer

Implemented token recognition for identifiers, constants, strings, keywords, and language symbols.

### Version 2: Parser and Semantic Analysis

Added recursive-descent parsing, parse tree construction, formatted program traversal, scope handling, and semantic validation.

### Version 3: Interpreter

Added scoped memory, expression evaluation, object references, control-flow execution, file-based input, and runtime error handling.

## Technologies

* Python
* Recursive-descent parsing
* Compiler and interpreter design
* Abstract syntax and parse trees
* Scope and memory management
