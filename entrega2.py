import sys

class Token:
    def __init__(self, type, value):
        self.type = type  
        self.value = value  

class Tokenizer:
    def __init__(self, source):
        #self.source = source.replace(" ", "")
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
        #print(f"teste: {result}")


        while self.current_token.type == "PLUS" or self.current_token.type == "MINUS":
            op = self.current_token.type 
            self.tokenizer.selectNext() 
            self.current_token = self.tokenizer.current_token

            if self.current_token.type != 'NUMBER':
                raise ValueError("Era esperado um número.")
            if op == 'PLUS':
                result += self.parseTerm()
            elif op == 'MINUS':
                result -= self.parseTerm()

            #print(f"teste: {result}")

        return result

    def parseTerm(self):
        result = 0  

        if self.current_token.type == 'NUMBER':
            result = self.current_token.value
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token
        else:
            raise ValueError("A expressão deve começar com um número")

        while self.current_token.type == "MULT" or self.current_token.type == "DIV":
            op = self.current_token.type 
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token
            if self.current_token.type != 'NUMBER':
                raise ValueError("Era esperado um número.")
            if op == 'MULT':
                result *= self.current_token.value
            elif op == 'DIV':
                if self.current_token.value == 0:
                    raise ValueError("Divisão por zero não permitida.")
                result //= self.current_token.value
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.current_token

            #print(f"teste: {result}")

        return result

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
