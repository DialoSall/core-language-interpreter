import sys
from Scanner import Scanner
from Parser import Parser
from SemanticChecker import SemanticChecker
from Executor import Executor


def main():
    if len(sys.argv) != 3:
        print("ERROR: Expected code file and data file")
        return

    try:
        code_file = sys.argv[1]
        data_file = sys.argv[2]

        # Create scanner for the .code file
        scanner = Scanner(code_file)

        # Parse input and build parse tree
        parser = Parser(scanner)
        parse_tree = parser.parse_procedure()

        # Keep semantic checks from last version
        checker = SemanticChecker()
        checker.check(parse_tree)

        # Execute program using .data file
        executor = Executor(data_file)
        executor.execute_procedure(parse_tree)

    except Exception as e:
        message = str(e)

        if message.startswith("ERROR:"):
            print(message)
        elif message.startswith("Error:"):
            print("ERROR:" + message[6:])
        else:
            print("ERROR:", message)


if __name__ == "__main__":
    main()