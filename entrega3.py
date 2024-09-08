import sys

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
                result += self.parseTerm()
            elif op == 'MINUS':
                result -= self.parseTerm()

        return result

    def parseTerm(self):
        result = self.parseFactor()
        while self.current_token.type == "MULT" or self.current_token.type == "DIV":
            op = self.current_token.type 
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token

            if op == 'MULT':
                result *= self.parseFactor()
            elif op == 'DIV':
                divisor = self.parseFactor()
                if divisor == 0:
                    raise ValueError("Divisão por zero não permitida.")
                result //= divisor

        return result

    def parseFactor(self):
        if self.current_token.type == 'PLUS':
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token
            return self.parseFactor()  # Unary plus, no change
        elif self.current_token.type == 'MINUS':
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token
            return -self.parseFactor()  # Unary minus
        elif self.current_token.type == 'NUMBER':
            value = self.current_token.value
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token
            return value
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
        tokenizer = Tokenizer(codigo)  
        parser = Parser(tokenizer)  
        result = parser.parseExpression()  

        if tokenizer.current_token.type != 'EOF':
            raise ValueError("Erro: Esperado EOF no final da expressão.")

        return result

if __name__ == '__main__':
    operacao = sys.argv[1]
    result = Parser.run(operacao)
    print(result)
