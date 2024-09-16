import sys
import os
import re

class Token:
    def __init__(self, type, value):
        self.type = type  
        self.value = value  

class PrePro:
    @staticmethod
    def filter(source_code: str) -> str:
        filtered_code = ""
        index = 0
        while index < len(source_code):
            if source_code[index:index+2] == "/*":
                end_comment = source_code.find("*/", index + 2)
                if end_comment == -1:
                    raise Exception("Comentário inválido")
                index = end_comment + 2
            else:
                filtered_code += source_code[index]
                index += 1
        return filtered_code

class Tokenizer:
    def __init__(self, source):
        self.source = source  
        self.position = 0  
        self.next = None  
        self.selectNext() 

    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position] in [' ', '\n', '\t']:
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token('EOF', None)
            return

        caractere = self.source[self.position]

        if caractere == '+':
            self.next = Token('ADD', '+')
            self.position += 1
        elif caractere == '-':
            self.next = Token('SUB', '-')
            self.position += 1
        elif caractere == '*':
            self.next = Token('MULT', '*')
            self.position += 1
        elif caractere == '/':
            self.next = Token('DIV', '/')
            self.position += 1
        elif caractere == '(':
            self.next = Token('LPAREN', '(')
            self.position += 1
        elif caractere == ')':
            self.next = Token('RPAREN', ')')
            self.position += 1
        elif caractere == '{':
            self.next = Token('LBRACE', '{')
            self.position += 1
        elif caractere == '}':
            self.next = Token('RBRACE', '}')
            self.position += 1
        elif caractere == ';':
            self.next = Token('SEMI', ';')
            self.position += 1
        elif caractere == '=':
            self.next = Token('ASSIGN', '=')
            self.position += 1
        elif caractere.isdigit():
            start = self.position
            while self.position < len(self.source) and self.source[self.position].isdigit():
                self.position += 1
            self.next = Token('INT', int(self.source[start:self.position]))
        elif caractere.isalpha() or caractere == '_':
            start = self.position
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                self.position += 1
            identifier = self.source[start:self.position]
            if identifier == 'printf':
                self.next = Token('PRINTF', identifier)
            else:
                self.next = Token('IDENT', identifier)
        else:
            raise ValueError(f"Caractere inválido '{caractere}' na posição {self.position}")

class SymbolTable:
    def __init__(self):
        self.table = {}

    def getter(self, identifier):
        if identifier in self.table:
            return self.table[identifier]
        else:
            raise ValueError(f"Identificador '{identifier}' não encontrado")

    def setter(self, identifier, value):
        self.table[identifier] = value

class Node:
    def Evaluate(self, symbol_table):
        pass

class BinOp(Node):
    def __init__(self, type, left, right):
        self.type = type
        self.left = left
        self.right = right

    def Evaluate(self, symbol_table):
        left_value = self.left.Evaluate(symbol_table)
        right_value = self.right.Evaluate(symbol_table)
        if self.type == "ADD":
            return left_value + right_value
        elif self.type == "SUB":
            return left_value - right_value
        elif self.type == "MULT":
            return left_value * right_value
        elif self.type == "DIV":
            if right_value == 0:
                raise ValueError("Divisão por zero")
            return left_value // right_value

class UnOp(Node):
    def __init__(self, type, child):
        self.type = type
        self.child = child

    def Evaluate(self, symbol_table):
        child_value = self.child.Evaluate(symbol_table)
        if self.type == "ADD":
            return +child_value
        elif self.type == "SUB":
            return -child_value

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self, symbol_table):
        return self.value

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

class NoOp(Node):
    def Evaluate(self, symbol_table):
        pass

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
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        tokenizer.selectNext()

    def parseProgram(self):
        result = self.parseBlock()
        if self.tokenizer.next.type != 'EOF':
            raise ValueError("Tokens inesperados após o fim do programa")
        return result

    def parseBlock(self):
        if self.tokenizer.next.type != 'LBRACE':
            raise ValueError("Esperado '{' no início do bloco")
        self.tokenizer.selectNext()
        statements = Statements()
        while self.tokenizer.next.type != 'RBRACE':
            statements.statements.append(self.parseStatement())
        self.tokenizer.selectNext()
        return statements

    def parseStatement(self):
        if self.tokenizer.next.type == 'SEMI':
            self.tokenizer.selectNext()
            return NoOp()
        elif self.tokenizer.next.type == 'PRINTF':
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != 'LPAREN':
                raise ValueError("Esperado '(' após 'printf'")
            self.tokenizer.selectNext()
            expr = self.parseExpression()
            if self.tokenizer.next.type != 'RPAREN':
                raise ValueError("Esperado ')' após expressão em 'printf'")
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != 'SEMI':
                raise ValueError("Esperado ';' após 'printf'")
            self.tokenizer.selectNext()
            return Print(expr)
        elif self.tokenizer.next.type == 'IDENT':
            identifier = Identifier(self.tokenizer.next.value)
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != 'ASSIGN':
                raise ValueError("Esperado '=' após identificador")
            self.tokenizer.selectNext()
            expr = self.parseExpression()
            if self.tokenizer.next.type != 'SEMI':
                raise ValueError("Esperado ';' após expressão")
            self.tokenizer.selectNext()
            return Assignment(identifier, expr)
        else:
            raise ValueError(f"Declaração inválida: '{self.tokenizer.next.value}'")

    def parseExpression(self):
        result = self.parseTerm()
        while self.tokenizer.next.type in ['ADD', 'SUB']:
            op_type = self.tokenizer.next.type
            self.tokenizer.selectNext()
            result = BinOp(op_type, result, self.parseTerm())
        return result

    def parseTerm(self):
        result = self.parseFactor()
        while self.tokenizer.next.type in ['MULT', 'DIV']:
            op_type = self.tokenizer.next.type
            self.tokenizer.selectNext()
            result = BinOp(op_type, result, self.parseFactor())
        return result

    def parseFactor(self):
        if self.tokenizer.next.type == 'INT':
            result = IntVal(self.tokenizer.next.value)
            self.tokenizer.selectNext()
            return result
        elif self.tokenizer.next.type == 'IDENT':
            result = Identifier(self.tokenizer.next.value)
            self.tokenizer.selectNext()
            return result
        elif self.tokenizer.next.type in ['ADD', 'SUB']:
            op_type = self.tokenizer.next.type
            self.tokenizer.selectNext()
            return UnOp(op_type, self.parseFactor())
        elif self.tokenizer.next.type == 'LPAREN':
            self.tokenizer.selectNext()
            result = self.parseExpression()
            if self.tokenizer.next.type != 'RPAREN':
                raise ValueError("Esperado ')'")
            self.tokenizer.selectNext()
            return result
        else:
            raise ValueError(f"Token inesperado: '{self.tokenizer.next.type}'")

    @staticmethod
    def run(filtered_code: str):
        tokenizer = Tokenizer(filtered_code)
        parser = Parser(tokenizer)
        result = parser.parseProgram()
        return result

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as file:
        source = file.read()
    filtered_code = PrePro.filter(source)
    ast = Parser.run(filtered_code)
    symbol_table = SymbolTable()
    ast.Evaluate(symbol_table)
