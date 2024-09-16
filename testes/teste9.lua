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
        elif caractere.isdigit():
            value = 0
            while self.position < len(self.source) and self.source[self.position].isdigit():
                value = value * 10 + int(self.source[self.position]) 
                self.position += 1
            self.current_token = Token('NUMBER', value)
        elif caractere.isalpha():
            identifier = ''
            while self.position < len(self.source) and self.source[self.position].isalnum():
                identifier += self.source[self.position]
                self.position += 1
            if identifier == 'printf':
                self.current_token = Token('PRINTF', 'printf')
            else:
                self.current_token = Token('IDENTIFIER', identifier)
        elif caractere == '=':
            self.current_token = Token('ASSIGN', '=')
            self.position += 1
        else:
            raise ValueError(f"Caractere desconhecido: {caractere}")

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
        self.symbols = {}

    def get(self, name):
        return self.symbols.get(name)

    def set(self, name, value):
        self.symbols[name] = value

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

class Printf(Node):
    def __init__(self, child):
        super().__init__('PRINTF')
        self.children = [child]

    def Evaluate(self, symbol_table):
        print(self.children[0].Evaluate(symbol_table))

class Identifier(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self, symbol_table):
        value = symbol_table.get(self.value)
        if value is None:
            raise ValueError(f"Variável '{self.value}' não definida.")
        return value

class Assignment(Node):
    def __init__(self, identifier, expression):
        super().__init__('ASSIGN')
        self.children = [identifier, expression]

    def Evaluate(self, symbol_table):
        identifier = self.children[0].value
        value = self.children[1].Evaluate(symbol_table)
        symbol_table.set(identifier, value)

class Block(Node):
    def __init__(self):
        super().__init__('BLOCK')

    def Evaluate(self, symbol_table):
        for child in self.children:
            child.Evaluate(symbol_table)

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer 
        self.current_token = tokenizer.current_token 

    def parseBlock(self):
        block = Block()
        if self.current_token.type == 'LBRACE':
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token
            while self.current_token.type != 'RBRACE':
                block.children.append(self.parseStatement())
                self.current_token = self.tokenizer.current_token
            self.tokenizer.selectNext()
        else:
            raise ValueError("Erro: Bloco esperado")
        return block

    def parseStatement(self):
        if self.current_token.type == 'IDENTIFIER':
            identifier = Identifier(self.current_token.value)
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token
            if self.current_token.type == 'ASSIGN':
                self.tokenizer.selectNext()
                self.current_token = self.tokenizer.current_token
                expression = self.parseExpression()
                return Assignment(identifier, expression)
            else:
                raise ValueError("Erro: '=' esperado")
        elif self.current_token.type == 'PRINTF':
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token
            if self.current_token.type == 'EPARENT':
                self.tokenizer.selectNext()
                self.current_token = self.tokenizer.current_token
                expression = self.parseExpression()
                if self.current_token.type == 'DPARENT':
                    self.tokenizer.selectNext()
                    self.current_token = self.tokenizer.current_token
                    return Printf(expression)
                else:
                    raise ValueError("Erro: ')' esperado após printf")
            else:
                raise ValueError("Erro: '(' esperado após printf")
        else:
            return NoOp()

    def parseExpression(self):
        result = self.parseTerm()
        while self.current_token.type == "PLUS" or self.current_token.type == "MINUS":
            op = self.current_token.type 
            self.tokenizer.selectNext() 
            self.current_token = self.tokenizer.current_token

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
        if self.current_token.type == 'PLUS':
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token
            return UnOp('PLUS', self.parseFactor()) 
        elif self.current_token.type == 'MINUS':
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token
            return UnOp('MINUS', self.parseFactor())  
        elif self.current_token.type == 'NUMBER':
            value = self.current_token.value
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token
            return IntVal(value)
        elif self.current_token.type == 'EPARENT':
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token
            result = self.parseExpression()
            if self.current_token.type != 'DPARENT':
                raise ValueError("Erro: Esperado ')'")
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token
            return result
        elif self.current_token.type == 'IDENTIFIER':
            identifier = Identifier(self.current_token.value)
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token
            return identifier
        else:
            raise ValueError("Erro: Token inesperado")

    @staticmethod
    def run(codigo):
        codigo = PrePro.filter(codigo)
        tokenizer = Tokenizer(codigo)  
        parser = Parser(tokenizer)  
        result = parser.parseBlock()  

        if tokenizer.current_token.type != 'EOF':
            raise ValueError("Erro: Esperado EOF no final da expressão.")

        return result

if __name__ == '__main__':

    arquivo = sys.argv[1]

    with open(arquivo, 'r') as file:
        operacao = file.read()

    symbol_table = SymbolTable()
    ast = Parser.run(operacao)
    resultado = ast.Evaluate(symbol_table)
    print(resultado)
