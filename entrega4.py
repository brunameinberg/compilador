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
        elif caractere.isdigit():
            value = 0
            while self.position < len(self.source) and self.source[self.position].isdigit():
                value = value * 10 + int(self.source[self.position]) 
                self.position += 1
            self.current_token = Token('NUMBER', value)
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
    

class Node:
    def __init__(self, value=None):
        self.value = value
        self.children = []

    def Evaluate(self):
        pass

class BinOp(Node):
    def __init__(self, value, left, right):
        super().__init__(value)
        self.children = [left, right]

    def Evaluate(self):
        left_value = self.children[0].Evaluate()
        right_value = self.children[1].Evaluate()
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

    def Evaluate(self):
        child_value = self.children[0].Evaluate()
        if self.value == 'PLUS':
            return child_value
        elif self.value == 'MINUS':
            return -child_value

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self):
        return self.value

class NoOp(Node):
    def Evaluate(self):
        return 0
      
class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer 
        self.current_token = tokenizer.current_token 

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
        else:
            raise ValueError("Erro: Token inesperado")

    @staticmethod
    def run(codigo):
        codigo = PrePro.filter(codigo)
        tokenizer = Tokenizer(codigo)  
        parser = Parser(tokenizer)  
        result = parser.parseExpression()  

        if tokenizer.current_token.type != 'EOF':
            raise ValueError("Erro: Esperado EOF no final da expressão.")

        return result

if __name__ == '__main__':

    arquivo = sys.argv[1]

    with open(arquivo, 'r') as file:
        operacao = file.read()

    ast = Parser.run(operacao)
    resultado = ast.Evaluate()
    print(resultado)
