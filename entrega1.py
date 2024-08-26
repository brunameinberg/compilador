import sys

class Token():
    def __init__(self, type, value):
        self.type = type  
        self.value = value  

class Tokenizer():
    def __init__(self, source):
        self.source = source.replace(" ", "")  # operação ""fonte""" sem espaços
        self.position = 0  
        self.next = None  
        self.selectNext() 

    def selectNext(self):
    
        # Quando acabar a operação
        if self.position >= len(self.source):
            self.next = Token('EOF', None) # token EOF a pedido
            return

        caractere = self.source[self.position] 

        # Identifica o tipo de token e atualiza o próximo token
        if caractere == '+':
            self.next = Token('PLUS', '+')
            self.position += 1
        elif caractere == '-':
            self.next = Token('MINUS', '-')
            self.position += 1
        elif caractere.isdigit():
            if self.next and self.next.type == 'NUMBER':
                raise ValueError("hmmmm cade a operação?")
        
            value = 0
            
            while self.position < len(self.source) and self.source[self.position].isdigit():
                value = value * 10 + int(self.source[self.position]) 
                self.position += 1
            self.next = Token('NUMBER', value)
        else:
            raise ValueError(f"caractere estranho!: {caractere}")

class Parser():
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer 
        self.current_token = tokenizer.next # Token atual
        tokenizer.selectNext() 


    def parseExpression(self):
        result = 0  

        if self.current_token.type == 'NUMBER':
            result = self.current_token.value
            self.current_token = self.tokenizer.next 
            self.tokenizer.selectNext()
        else:
            raise ValueError("A expressão deve começar com um número")

        while self.current_token.type == 'PLUS' or self.current_token.type ==  'MINUS':
            op = self.current_token.type 
            self.current_token = self.tokenizer.next 
            self.tokenizer.selectNext()
            if self.current_token.type != 'NUMBER':
                raise ValueError("Era pra ser um numero...")
            if op == 'PLUS':
                result += self.current_token.value
            elif op == 'MINUS':
                result -= self.current_token.value
            self.current_token = self.tokenizer.next  
            self.tokenizer.selectNext()
    


        return result

    @staticmethod
    def run(codigo):
        tokenizer = Tokenizer(codigo)  
        parser = Parser(tokenizer)  
        result = parser.parseExpression()  

        if tokenizer.next.type != 'EOF':
            raise ValueError("Erro")

        return result

if __name__ == '__main__':
    operacao = sys.argv[1]
    result = Parser.run(operacao)
    print(result)
