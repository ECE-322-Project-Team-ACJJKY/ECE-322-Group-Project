import ast
import random
import os


class UnknownConstant(Exception):
    pass


class UnknownCompare(Exception):
    pass


class ConstantVisitor(ast.NodeVisitor):
    def __init__(self):
        self.line_nos = []

    def visit_Constant(self, node):
        if isinstance(node.value, str) or isinstance(node.value, int) or isinstance(node.value, float):
            self.line_nos.append(node.lineno)
        return node
    

class CompareVisitor(ast.NodeVisitor):
    def __init__(self):
        self.line_nos = []
    
    def visit_Compare(self, node):
        self.line_nos.append(node.lineno)


class StatementVisitor(ast.NodeVisitor):
    def __init__(self):
        self.line_nos = []
    
    def generic_visit(self, node):
        if hasattr(node, "lineno"):
            if not (node.lineno in self.line_nos):
                self.line_nos.append(node.lineno)
        return super().generic_visit(node)


class ValueTransformer(ast.NodeTransformer):
    def __init__(self, target_lineno):
        self.target_lineno = target_lineno

    def visit_Constant(self, node):
        def mutate(constant):
            if isinstance(constant.value, str):
                print(f"Transforming string {constant.value}")
                mutant_string = constant.value
                while mutant_string == constant.value:
                    mutant_string  = "".join([random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(len(constant.value))])
                return ast.Constant(mutant_string)

            if isinstance(constant.value, int):
                print(f"Transforming int {constant.value}")
                mutant_int = constant.value
                while mutant_int == constant.value:
                    mutant_int = random.randint(-100, 100)
                return ast.Constant(mutant_int)

            if isinstance(constant.value, float):
                print(f"Transforming float {constant.value}")
                mutant_float = constant.value
                while mutant_float == constant.value:
                    mutant_float = random.randint(-100, 100) * random.random()
                return ast.Constant(mutant_float)

            raise UnknownConstant(f"Tried mutating unknown constant {constant.value}")

        if node.lineno == self.target_lineno:
            node.value = mutate(node).value

        return node


class DecisionTransformer(ast.NodeTransformer):
    def __init__(self, target_lineno):
        self.target_lineno = target_lineno
    
    def visit_Compare(self, node):
        def mutate(operator):
            if isinstance(operator, ast.Eq):
                return ast.NotEq()
            elif isinstance(operator, ast.NotEq):
                return ast.Eq()
            elif isinstance(operator, ast.Lt):
                return ast.LtE()
            elif isinstance(operator, ast.LtE):
                return ast.Lt()
            elif isinstance(operator, ast.Gt):
                return ast.GtE()
            elif isinstance(operator, ast.GtE):
                return ast.Gt()
            elif isinstance(operator, ast.Is):
                return ast.IsNot()
            elif isinstance(operator, ast.IsNot):
                return ast.Is()
            elif isinstance(operator, ast.In):
                return ast.NotIn()
            elif isinstance(operator, ast.NotIn):
                return ast.In()
            raise UnknownCompare(f"Unknown compare operator: {operator}")
        
        if node.lineno == self.target_lineno:
            new_ops = []
            for op in node.ops: 
                new_ops.append(mutate(op))
            node.ops = new_ops

        return node


class StatementTransformer(ast.NodeTransformer):
    def __init__(self, target_lineno):
        self.target_lineno = target_lineno

    def generic_visit(self, node):
        if hasattr(node, "lineno"):
            if node.lineno == self.target_lineno:
                return None
        return super().generic_visit(node)


def generate_value_mutants(filename):
    with open(filename, "r") as f:
        print(f"=== {filename} ===")
        source_file_contents = f.read()

    visitor = ConstantVisitor()
    tree = ast.parse(source_file_contents)
    visitor.visit(tree)

    file_basename = os.path.splitext(os.path.basename(filename))[0]
    for lineno in visitor.line_nos:
        print(f"Running transformer on {filename}:{lineno}")
        try:
            tree = ast.parse(source_file_contents)
            transformer = ValueTransformer(lineno)
            transformed_tree = transformer.visit(tree)

            new_mutant_filename = f"./tests/mutants/value_mutants/{file_basename}_{lineno}"
            with open(new_mutant_filename, "w+") as f:
                f.write(ast.unparse(transformed_tree))
        except UnknownConstant as e:
            print(f"{e}")


def generate_decision_mutants(filename):
    with open(filename, "r") as f:
        print(f"=== {filename} ===")
        source_file_contents = f.read()

    visitor = CompareVisitor()
    tree = ast.parse(source_file_contents)
    visitor.visit(tree)

    file_basename = os.path.splitext(os.path.basename(filename))[0]
    for lineno in visitor.line_nos:
        print(f"Running transformer on {filename}:{lineno}")
        try:
            tree = ast.parse(source_file_contents)
            transformer = DecisionTransformer(lineno)
            transformed_tree = transformer.visit(tree)

            new_mutant_filename = f"./tests/mutants/decision_mutants/{file_basename}_{lineno}"
            with open(new_mutant_filename, "w+") as f:
                f.write(ast.unparse(transformed_tree))
        except UnknownCompare as e:
            print(f"{e}")


def generate_statement_mutants(filename):
    with open(filename, "r") as f:
        print(f"=== {filename} ===")
        source_file_contents = f.read()

    visitor = StatementVisitor()
    tree = ast.parse(source_file_contents)
    visitor.visit(tree)

    file_basename = os.path.splitext(os.path.basename(filename))[0]
    for lineno in visitor.line_nos:
        print(f"Running transformer on {filename}:{lineno}")
        try:
            tree = ast.parse(source_file_contents)
            transformer = StatementTransformer(lineno)
            transformed_tree = transformer.visit(tree)

            new_mutant_filename = f"./tests/mutants/statement_mutants/{file_basename}_{lineno}"
            try:
                mutant_code = ast.unparse(transformed_tree)
                with open(new_mutant_filename, "w+") as f:
                    f.write(mutant_code)
            except Exception as e:
                print(e)

        except UnknownCompare as e:
            print(f"{e}")


if __name__ == "__main__":
    source_files = [
        "./wordle/defaults.py", 
        "./wordle/evaluate.py", 
        "./wordle/solver.py", 
        "./wordle/vocab.py", 
        "./wordle/wordle.py"
    ]

    for filename in source_files:
        generate_value_mutants(filename)
        generate_decision_mutants(filename)
        generate_statement_mutants(filename)
