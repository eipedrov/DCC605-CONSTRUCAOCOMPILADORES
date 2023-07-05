class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, ast):
        self.visit(ast)

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise NotImplementedError(f'Visit method not implemented for {type(node).__name__}')

    def visit_Assignment(self, node):
        variable_name = node.variable
        if variable_name in self.symbol_table:
            raise Exception(f'Variable "{variable_name}" already declared')
        self.symbol_table[variable_name] = None

        self.visit(node.value)

    def visit_BinaryOperation(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Variable(self, node):
        variable_name = node.name
        if variable_name not in self.symbol_table:
            raise Exception(f'Variable "{variable_name}" is not declared')

    def print_ast(self, node, indent=''):
        print(indent + type(node).__name__)
        if isinstance(node, Assignment):
            print(indent + '  Variavel:', node.variable)
            print(indent + '  Valor:')
            self.print_ast(node.value, indent + '    ')
        elif isinstance(node, BinaryOperation):
            print(indent + '  Operador:', node.operator)
            print(indent + '  Operador Esquerdo:')
            self.print_ast(node.left, indent + '    ')
            print(indent + '  Operador Direito:')
            self.print_ast(node.right, indent + '    ')
        elif isinstance(node, Variable):
            print(indent + '  Nome:', node.name)

# Exemplo de uso
class Assignment:
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

class BinaryOperation:
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator

class Variable:
    def __init__(self, name):
        self.name = name

# Criação da AST
assignment = Assignment(Variable("x"), BinaryOperation(Variable("y"), Variable("z"), "+"))

# Criação do analisador semântico
analyzer = SemanticAnalyzer()

# Adicionando declaração das variáveis na tabela de símbolos
analyzer.symbol_table["y"] = None
analyzer.symbol_table["z"] = None

# Execução da análise semântica
analyzer.analyze(assignment)

# Impressão da AST
analyzer.print_ast(assignment)
