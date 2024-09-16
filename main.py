import sys
import os
import re


class Token:
    def __init__(self, type, value):
        self.type = type  
        self.value = value  

class Tokenizer:
    def __init__(self, source):
        self.source = source  
        self.position = 0  
        self.current_token = None  
        self.selectNext() 

    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position] == ' ':
            self.position += 1

        if self.position >= len(self.source):
            self.current_token = Token('EOF', None) 
            return

        caractere = self.source[self.position] 

        if caractere == '+':
            self.current_token = Token('PLUS', '+')
            self.position += 1
        elif caractere == '-':
            self.current_token = Token('MINUS', '-')
            self.position += 1
        elif caractere == '*':
            self.current_token = Token('MULT', '*')
            self.position += 1
        elif caractere == '/':
            self.current_token = Token('DIV', '/')
            self.position += 1
        elif caractere == '(':
            self.current_token = Token('EPARENT', '(')
            self.position += 1
        elif caractere == ')':
            self.current_token = Token('DPARENT', ')')
            self.position += 1
        elif caractere == '{':
            self.current_token = Token('LBRACE', '{')
            self.position += 1
        elif caractere == '}':
            self.current_token = Token('RBRACE', '}')
            self.position += 1
        elif caractere == ';':
            self.current_token = Token('SEMICOLON', ';')
            self.position += 1
        elif caractere == '=':
            self.current_token = Token('EQUAL', '=')
            self.position += 1
        elif caractere.isdigit():
            start = self.position
            while self.position < len(self.source) and self.source[self.position].isdigit():
                self.position += 1
            self.current_token = Token("NUMBER", int(self.source[start:self.position]))
        elif caractere.isalpha() or caractere == '_':
            start = self.position
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                self.position += 1
            identifier = self.source[start:self.position]
            if identifier == 'printf':
                self.current_token = Token("PRINTF", identifier)
            else:
                self.current_token = Token("IDENT", identifier)
        else:
            raise Exception(f"Erro: Caractere inesperado encontrado: {caractere}")


class PrePro:
    @staticmethod
    def filter(source):
        lines = source.splitlines()
        filtered_lines = [line.split('#')[0].strip() for line in lines]
        filtered_source = ' '.join(filtered_lines)
        
        filtered_source = re.sub(r'/\*.*?\*/', '', filtered_source, flags=re.DOTALL)
        
        return filtered_source
    
class SymbolTable:
    def __init__(self):
        self.table = {}

    def getter(self, identifier):
        if identifier in self.table:
            return self.table[identifier]
        else:
            raise Exception(f"Erro: Identificador '{identifier}' não encontrado")

    def setter(self, identifier, value):
        self.table[identifier] = value

class Node:
    def __init__(self, value=None):
        self.value = value
        self.children = []

    def Evaluate(self, symbol_table):
        pass

class BinOp(Node):
    def __init__(self, value, left, right):
        super().__init__(value)
        self.children = [left, right]

    def Evaluate(self, symbol_table):
        left_value = self.children[0].Evaluate(symbol_table)
        right_value = self.children[1].Evaluate(symbol_table)
        if self.value == 'PLUS':
            return left_value + right_value
        elif self.value == 'MINUS':
            return left_value - right_value
        elif self.value == 'MULT':
            return left_value * right_value
        elif self.value == 'DIV':
            if right_value == 0:
                raise ValueError("Divisão por zero não permitida.")
            return left_value // right_value

class UnOp(Node):
    def __init__(self, value, child):
        super().__init__(value)
        self.children = [child]

    def Evaluate(self, symbol_table):
        child_value = self.children[0].Evaluate(symbol_table)
        if self.value == 'PLUS':
            return child_value
        elif self.value == 'MINUS':
            return -child_value

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self, symbol_table):
        return self.value

class NoOp(Node):
    def Evaluate(self, symbol_table):
        return 0

class Identifier(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self, symbol_table):
        return symbol_table.getter(self.value)
    
class Assignment(Node):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def Evaluate(self, symbol_table):
        value = self.expression.Evaluate(symbol_table)
        symbol_table.setter(self.identifier.value, value)

class Print(Node):
    def __init__(self, expression):
        self.expression = expression

    def Evaluate(self, symbol_table):
        value = self.expression.Evaluate(symbol_table)
        print(f"{value}")

class Statements(Node):
    def __init__(self):
        self.statements = []

    def Evaluate(self, symbol_table):
        for statement in self.statements:
            statement.Evaluate(symbol_table)



class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer 
        self.current_token = tokenizer.current_token 

    def parseProgram(self):
        result = self.parseBlock()
        if self.tokenizer.current_token.type != 'EOF':
            raise Exception("Erro: Tokens adicionais encontrados após o fim do programa")
        return result

    def parseBlock(self):
        if self.tokenizer.current_token.type != 'LBRACE':
            raise Exception("Erro: Esperado '{' no início do bloco")
        self.tokenizer.selectNext()
        statements = Statements()
        while self.tokenizer.current_token.type != 'RBRACE':
            statements.statements.append(self.parseStatement())
        self.tokenizer.selectNext()
        return statements
    
    def parseStatement(self):
        if self.tokenizer.current_token.type == 'SEMICOLON':
            self.tokenizer.selectNext()
            return NoOp()
        elif self.tokenizer.current_token.type == 'PRINTF':
            self.tokenizer.selectNext()  # Avança para o próximo token após 'PRINTF'
            if self.tokenizer.current_token.type != 'EPARENT':  
                raise Exception("Erro: Esperado '(' após 'printf'")
            self.tokenizer.selectNext()  # Avança após '('
            expr = self.parseExpression()
            if self.tokenizer.current_token.type != 'DPARENT': 
                raise Exception("Erro: Esperado ')' após expressão em 'printf'")
            self.tokenizer.selectNext()  # Avança após ')'
            if self.tokenizer.current_token.type != 'SEMICOLON':
                raise Exception("Erro: Esperado ';' após 'printf'")
            self.tokenizer.selectNext()  # Avança após ';'
            return Print(expr)
        elif self.tokenizer.current_token.type == 'IDENT':
            identifier = Identifier(self.tokenizer.current_token.value)
            self.tokenizer.selectNext()
            if self.tokenizer.current_token.type != 'EQUAL':
                raise Exception("Erro: Esperado '=' após identificador")
            self.tokenizer.selectNext()
            expr = self.parseExpression()
            if self.tokenizer.current_token.type != 'SEMICOLON':
                raise Exception("Erro: Esperado ';' após expressão")
            self.tokenizer.selectNext()
            return Assignment(identifier, expr)
        else:
            raise Exception(f"Erro: Declaração inválida: '{self.tokenizer.current_token.value}'")


    def parseExpression(self):
        result = self.parseTerm()
        while self.current_token.type == "PLUS" or self.current_token.type == "MINUS":
            op = self.current_token.type 
            self.tokenizer.selectNext() 
            self.current_token = self.tokenizer.selectNext()

            if op == 'PLUS':
                result = BinOp('PLUS', result, self.parseTerm())
            elif op == 'MINUS':
                result = BinOp('MINUS', result, self.parseTerm())

        return result

    def parseTerm(self):
        result = self.parseFactor()
        while self.current_token.type == "MULT" or self.current_token.type == "DIV":
            op = self.current_token.type 
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token

            if op == 'MULT':
                result = BinOp('MULT', result, self.parseFactor())
            elif op == 'DIV':
                divisor_node = self.parseFactor()
                result = BinOp('DIV', result, divisor_node)

        return result

    def parseFactor(self):
        if self.tokenizer.current_token.type == 'NUMBER':
            result = IntVal(self.tokenizer.current_token.value)
            self.tokenizer.selectNext()
            return result
        elif self.tokenizer.current_token.type == 'IDENT':
            result = Identifier(self.tokenizer.current_token.value)
            self.tokenizer.selectNext()
            return result
        elif self.tokenizer.current_token.type in ['PLUS', 'MINUS']:
            op_type = self.tokenizer.current_token.type
            self.tokenizer.selectNext()
            return UnOp(op_type, self.parseFactor())
        elif self.tokenizer.current_token.type == 'LPAREN':
            self.tokenizer.selectNext()
            result = self.parseExpression()
            if self.tokenizer.current_token.type != 'RPAREN':
                raise Exception("Erro: Esperado ')'")
            self.tokenizer.selectNext()
            return result
        else:
            raise Exception(f"Erro: Token inesperado: '{self.tokenizer.current_token.type}'")

    @staticmethod
    def run(codigo):
        codigo = PrePro.filter(codigo)
        tokenizer = Tokenizer(codigo)  
        parser = Parser(tokenizer)  
        result = parser.parseProgram()  

        if tokenizer.current_token.type != 'EOF':
            raise ValueError("Erro: Esperado EOF no final da expressão.")

        return result

if __name__ == '__main__':

    arquivo = sys.argv[1]

    with open(arquivo, 'r') as file:
        operacao = file.read()

    ast = Parser.run(operacao)
    symbol_table = SymbolTable()
    ast.Evaluate(symbol_table)
