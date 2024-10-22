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
            #caso for igual igual
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                self.current_token = Token('EQUALEQUAL', '==')
                self.position += 2
            else:
                self.current_token = Token('EQUAL', '=')
                self.position += 1
        elif caractere == 's':
            start = self.position
            while self.position < len(self.source) and self.source[self.position].isalpha():
                self.position += 1
            identifier = self.source[start:self.position]
            if identifier == 'string' or identifier == 'str':
                self.current_token = Token("STRING_TYPE", identifier)
            else:
                raise Exception(f"Erro: Token inesperado: '{identifier}'")
        elif caractere == '<':
            self.current_token = Token('LESS', '<')
            self.position += 1
        elif caractere == '>':
            self.current_token = Token('GREATER', '>')
            self.position += 1
        elif caractere == '|':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '|':
                self.current_token = Token('OR', '||')
                self.position += 2
            else:
                raise Exception(f"Erro: Token inesperado: '{caractere}'")
        elif caractere == '&':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '&':
                self.current_token = Token('AND', '&&')
                self.position += 2
            else:
                raise Exception(f"Erro: Token inesperado: '{caractere}'")
        elif caractere == 'i':
            start = self.position
            while self.position < len(self.source) and self.source[self.position].isalpha():
                self.position += 1
            identifier = self.source[start:self.position]
            if identifier == 'if':
                self.current_token = Token("IF", identifier)
            elif identifier == 'int':
                self.current_token = Token("INT_TYPE", identifier)
            else:
                self.current_token = Token("IDENT", identifier)
        elif caractere == 'e':
            start = self.position
            while self.position < len(self.source) and self.source[self.position].isalpha():
                self.position += 1
            identifier = self.source[start:self.position]
            if identifier == 'else':
                self.current_token = Token("ELSE", identifier)
            else:
                self.current_token = Token("IDENT", identifier)
        elif caractere == 'w':
            start = self.position
            while self.position < len(self.source) and self.source[self.position].isalpha():
                self.position += 1
            identifier = self.source[start:self.position]
            if identifier == 'while':
                self.current_token = Token("WHILE", identifier)
            else:
                raise Exception(f"Erro: Token inesperado: '{identifier}'")
        elif caractere == '!':
            self.current_token = Token('NOT', '!')
            self.position += 1
        
        elif caractere == '"':
            start = self.position + 1
            end = self.source.find('"', start)
            if end == -1:
                raise Exception("Erro: String não fechada")
            string_value = self.source[start:end]
            self.current_token = Token("STRING", string_value)
            self.position = end + 1

        elif caractere == 'b':
            start = self.position
            while self.position < len(self.source) and self.source[self.position].isalpha():
                self.position += 1
            identifier = self.source[start:self.position]
            if identifier == 'bool':
                self.current_token = Token("BOOL_TYPE", identifier)  # Identificamos o tipo bool
            else:
                self.current_token = Token("IDENT", identifier)

        elif caractere == ',':
            self.current_token = Token("COMMA", ',')  # Corrigimos para retornar um token de vírgula corretamente
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
            return self.table[identifier]  # Retorna (value, var_type, offset)
        else:
            raise Exception(f"Erro: Identificador '{identifier}' não encontrado")

    def setter(self, identifier, value, var_type, offset):
        self.table[identifier] = (value, var_type, offset)

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
        CodeGenerator.emit("PUSH EBX")
        right_value = self.children[1].Evaluate(symbol_table)
        CodeGenerator.emit("POP EAX")


        if self.value == 'PLUS':
            CodeGenerator.emit("ADD EAX, EBX")

        elif self.value == 'MINUS':
            CodeGenerator.emit("SUB EAX, EBX")

        elif self.value == 'MULT':
            CodeGenerator.emit("IMUL EAX, EBX")

        elif self.value == 'DIV':
            CodeGenerator.emit("IDIV EBX")
        
        elif self.value == 'EQUALEQUAL':
            CodeGenerator.emit("CALL binop_je")  # Chama a subrotina de comparação
        elif self.value == 'LESS':
            CodeGenerator.emit("CALL binop_jl")
        elif self.value == 'GREATER':
            CodeGenerator.emit("CALL binop_jg")
        
        elif self.value == 'OR':
            CodeGenerator.emit("OR EAX, EBX")  # OR lógico entre EAX e EBX
            CodeGenerator.emit("MOV EBX, EAX")  # Armazena o resultado em EBX
        
        elif self.value == 'AND':
            CodeGenerator.emit("AND EAX, EBX")  # AND lógico entre EAX e EBX
            CodeGenerator.emit("MOV EBX, EAX")  # Armazena o resultado em EBX
        
        elif self.value == 'WHILE':
            loop_start = CodeGenerator.new_label("LOOP")
            loop_end = CodeGenerator.new_label("EXIT")
            CodeGenerator.emit(f"{loop_start}:")
            self.children[0].Evaluate(symbol_table)
            CodeGenerator.emit("CMP EBX, False")
            CodeGenerator.emit(f"JE {loop_end}")
            self.children[1].Evaluate(symbol_table)
            CodeGenerator.emit(f"JMP {loop_start}")
            CodeGenerator.emit(f"{loop_end}:")
        else:
            raise Exception(f"Operador desconhecido: {self.value}")

class UnOp(Node):
    def __init__(self, value, child):
        super().__init__(value)
        self.children = [child]

    def Evaluate(self, symbol_table):
        child_value = self.children[0].Evaluate(symbol_table)

        if self.value == 'PLUS':
            return
        
        elif self.value == 'MINUS':
            CodeGenerator.emit("NEG EBX")
        
        elif self.value == 'NOT':
            CodeGenerator.emit("CMP EBX, False")  # Compara EBX com False (0)
            
            # Geração de labels para controle de fluxo
            label_true = CodeGenerator.new_label("unop_true")
            label_exit = CodeGenerator.new_label("unop_exit")
            
            # Se EBX for igual a False, pula para o label que define True
            CodeGenerator.emit(f"JE {label_true}")
            
            # Caso contrário, define EBX como False
            CodeGenerator.emit("MOV EBX, False")
            CodeGenerator.emit(f"JMP {label_exit}")
            
            # Label que define EBX como True
            CodeGenerator.emit(f"{label_true}:")
            CodeGenerator.emit("MOV EBX, True")
            
            # Ponto de saída
            CodeGenerator.emit(f"{label_exit}:")

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self, symbol_table):
        CodeGenerator.emit(f"MOV EBX, {self.value}")

class NoOp(Node):
    def Evaluate(self, symbol_table):
        return 0

class Identifier(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self, symbol_table):
        value, var_type, offset = symbol_table.getter(self.value)  # Extrai os três valores
        return value
    
class Assignment(Node):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def Evaluate(self, symbol_table):
        value = self.expression.Evaluate(symbol_table)
        offset = 4 * (list(symbol_table.table.keys()).index(self.identifier.value) + 1)  # Calcula o deslocamento
        CodeGenerator.emit(f"MOV [EBP-{offset}], EBX")

class Print(Node):
    def __init__(self, expression):
        self.expression = expression

    def Evaluate(self, symbol_table):
        self.expression.Evaluate(symbol_table)  # O valor já está em EBX
        CodeGenerator.emit("PUSH EBX")
        CodeGenerator.emit("CALL print")
        CodeGenerator.emit("POP EBX")  # Limpa a pilha

class Statements(Node):
    def __init__(self):
        self.statements = []

    def Evaluate(self, symbol_table):
        for statement in self.statements:
            statement.Evaluate(symbol_table)

class If(Node):
    def __init__(self, condition, if_block, else_block=None):
        super().__init__('IF')
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block

    def Evaluate(self, symbol_table):
        if self.condition.Evaluate(symbol_table):  
            return self.if_block.Evaluate(symbol_table)
        elif self.else_block:  
            return self.else_block.Evaluate(symbol_table)
        return 0  

class VarDec(Node):
    def __init__(self, var_type, identifiers, expressions=None):
        super().__init__()
        self.var_type = var_type
        self.identifiers = identifiers
        self.expressions = expressions or []

    def Evaluate(self, symbol_table):
        for i, identifier in enumerate(self.identifiers):
            if identifier.value in symbol_table.table:
                raise Exception(f"Erro: Variável '{identifier.value}' já foi declarada")

            # Gera código para alocar a variável na pilha
            CodeGenerator.emit("PUSH DWORD 0")  # Alocação de espaço para a variável na pilha
            offset = 4 * (len(symbol_table.table) + 1)  # Calcula o deslocamento com base na posição atual
            symbol_table.setter(identifier.value, 0, self.var_type, offset)

            if i < len(self.expressions) and self.expressions[i] is not None:
                self.expressions[i].Evaluate(symbol_table)
                CodeGenerator.emit(f"MOV [EBP-{offset}], EBX") 

class StringVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self, symbol_table):
        string_label = CodeGenerator.new_label("string")
        CodeGenerator.emit(f"{string_label}: db '{self.value}', 0")  # Aloca a string na seção de dados
        CodeGenerator.emit(f"MOV EBX, {string_label}")


class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer 

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

        if self.tokenizer.current_token.type == 'LBRACE':
            return self.parseBlock()

        if self.tokenizer.current_token.type == 'SEMICOLON':
            self.tokenizer.selectNext()
            return NoOp()
        
        elif self.tokenizer.current_token.type == 'PRINTF':
            self.tokenizer.selectNext()  
            if self.tokenizer.current_token.type != 'EPARENT':
                raise Exception("Erro: Esperado '(' após 'printf'")
            self.tokenizer.selectNext()  
            expr = self.parseRelational()
            if self.tokenizer.current_token.type != 'DPARENT':
                raise Exception("Erro: Esperado ')' após expressão em 'printf'")
            self.tokenizer.selectNext()  
            if self.tokenizer.current_token.type != 'SEMICOLON':
                raise Exception("Erro: Esperado ';' após 'printf'")
            self.tokenizer.selectNext()  
            return Print(expr)
        
        elif self.tokenizer.current_token.type == 'IDENT':
            identifier = Identifier(self.tokenizer.current_token.value)
            self.tokenizer.selectNext()
            if self.tokenizer.current_token.type != 'EQUAL':
                raise Exception("Erro: Esperado '=' após identificador")
            self.tokenizer.selectNext()
            expr = self.parseRelational()
            if self.tokenizer.current_token.type != 'SEMICOLON':
                raise Exception("Erro: Esperado ';' após expressão")
            self.tokenizer.selectNext()
            return Assignment(identifier, expr)
        
        elif self.tokenizer.current_token.type == 'IF':
            self.tokenizer.selectNext()  
            if self.tokenizer.current_token.type != 'EPARENT':
                raise Exception("Erro: Esperado '(' após 'if'")
            self.tokenizer.selectNext()  
            condition = self.parseRelational()
            if self.tokenizer.current_token.type != 'DPARENT':
                raise Exception("Erro: Esperado ')' após expressão em 'if'")
            self.tokenizer.selectNext()
            
            if_block = self.parseBlock() if self.tokenizer.current_token.type == 'LBRACE' else self.parseStatement()

            else_block = None

            if self.tokenizer.current_token.type == 'ELSE':
                self.tokenizer.selectNext()
                else_block = self.parseBlock() if self.tokenizer.current_token.type == 'LBRACE' else self.parseStatement()

            return If(condition, if_block, else_block)
        
        elif self.tokenizer.current_token.type == 'WHILE':
            self.tokenizer.selectNext()  
            if self.tokenizer.current_token.type != 'EPARENT':
                raise Exception("Erro: Esperado '(' após 'while'")
            self.tokenizer.selectNext()  
            condition = self.parseRelational()
            if self.tokenizer.current_token.type != 'DPARENT':
                raise Exception("Erro: Esperado ')' após expressão em 'while'")
            self.tokenizer.selectNext()
            
            # Após o 'while', pode vir um bloco ou um statement
            block = self.parseStatement() if self.tokenizer.current_token.type != 'LBRACE' else self.parseBlock()
            
            return BinOp('WHILE', condition, block)
        
        if self.tokenizer.current_token.type == 'INT_TYPE':
            var_type = int
            self.tokenizer.selectNext()  
        elif self.tokenizer.current_token.type == 'STRING_TYPE':
            var_type = str
            self.tokenizer.selectNext()  
        elif self.tokenizer.current_token.type == 'BOOL_TYPE':
            var_type = bool
            self.tokenizer.selectNext()
        else:
            raise Exception(f"Erro: Tipo de variável inválido: {self.tokenizer.current_token.type}")

        identifiers = []
        expressions = []

        while self.tokenizer.current_token.type == 'IDENT':
            identifier = Identifier(self.tokenizer.current_token.value)
            identifiers.append(identifier)
            self.tokenizer.selectNext()

            if self.tokenizer.current_token.type == 'EQUAL':
                self.tokenizer.selectNext()
                expr = self.parseRelational()  # Avalia a expressão associada
                expressions.append(expr)
            else:
                expressions.append(None)  # Variável sem inicialização

            if self.tokenizer.current_token.type == 'COMMA':
                self.tokenizer.selectNext()  # Continuar declarando mais variáveis
            elif self.tokenizer.current_token.type == 'SEMICOLON':
                break  # Fim da declaração
            else:
                raise Exception(f"Erro: Esperado ',' ou ';', mas encontrado '{self.tokenizer.current_token.value}'")

        if self.tokenizer.current_token.type != 'SEMICOLON':
            raise Exception("Erro: Esperado ';' após declaração de variável")

        self.tokenizer.selectNext()  # Consumir o ponto e vírgula

        return VarDec(var_type, identifiers, expressions)

        # Verifica se o próximo token é uma chave de abertura
        if self.tokenizer.current_token.type == 'LBRACE':
            return self.parseBlock()
        else:
            raise Exception(f"Erro: Declaração inválida: '{self.tokenizer.current_token.value}'")


    def parseExpression(self):
        result = self.parseTerm()
        while self.tokenizer.current_token.type == "PLUS" or self.tokenizer.current_token.type == "MINUS" or self.tokenizer.current_token.type == "OR" or self.tokenizer.current_token.type == "NOT":
            op = self.tokenizer.current_token.type
            self.tokenizer.selectNext()  
            if op == 'PLUS':
                result = BinOp('PLUS', result, self.parseTerm())
            elif op == 'MINUS':
                result = BinOp('MINUS', result, self.parseTerm())
            elif op == 'OR':
                result = BinOp('OR', result, self.parseTerm())
            elif op == 'NOT':
                result = UnOp('NOT', self.parseTerm())
        return result


    def parseTerm(self):
        result = self.parseFactor()
        while self.tokenizer.current_token.type == "MULT" or self.tokenizer.current_token.type == "DIV" or self.tokenizer.current_token.type == "AND":
            op = self.tokenizer.current_token.type 
            self.tokenizer.selectNext()

            if op == 'MULT':
                result = BinOp('MULT', result, self.parseFactor())
            elif op == 'DIV':
                divisor_node = self.parseFactor()
                result = BinOp('DIV', result, divisor_node)
            elif op == 'AND':
                result = BinOp('AND', result, self.parseFactor())

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
        elif self.tokenizer.current_token.type == 'EPARENT':  
            self.tokenizer.selectNext()
            result = self.parseRelational()
            if self.tokenizer.current_token.type != 'DPARENT':  
                raise Exception("Erro: Esperado ')'")
            self.tokenizer.selectNext()
            return result
        elif self.tokenizer.current_token.type == 'NOT':
            self.tokenizer.selectNext()
            return UnOp('NOT', self.parseFactor())
        elif self.tokenizer.current_token.type == 'STRING':
            result = StringVal(self.tokenizer.current_token.value)  # Cria um nó para a string
            self.tokenizer.selectNext()
            return result
        else:
            raise Exception(f"Erro: Token inesperado: '{self.tokenizer.current_token.type}'")

    def parseRelational(self):
        result = self.parseExpression()
        if self.tokenizer.current_token.type in ['EQUALEQUAL', 'LESS', 'GREATER']:
            op = self.tokenizer.current_token.type
            self.tokenizer.selectNext()
            result = BinOp(op, result, self.parseExpression())
        return result


    @staticmethod
    def run(codigo):
        codigo = PrePro.filter(codigo)
        tokenizer = Tokenizer(codigo)  
        parser = Parser(tokenizer)  
        result = parser.parseProgram()  

        if tokenizer.current_token.type != 'EOF':
            raise ValueError("Erro: Esperado EOF no final da expressão.")

        return result

class CodeGenerator:
    instructions = []
    label_counter = 0

    @staticmethod
    def emit(instruction):
        CodeGenerator.instructions.append(instruction)

    @staticmethod
    def new_label(prefix="L"):
        label = f"{prefix}_{CodeGenerator.label_counter}"
        CodeGenerator.label_counter += 1
        return label

    @staticmethod
    def write_to_file(filename):
        # Cabeçalho inicial do código Assembly
        header = [
            "; constantes",
            "SYS_EXIT equ 1",
            "SYS_READ equ 3",
            "SYS_WRITE equ 4",
            "STDIN equ 0",
            "STDOUT equ 1",
            "True equ 1",
            "False equ 0",
            "",
            "segment .data",
            "",
            "segment .bss  ; variaveis",
            "  res RESB 1",
            "",
            "section .text",
            "  global _main",
            "",
            "print:  ; subrotina print",
            "  PUSH EBP ; guarda o base pointer",
            "  MOV EBP, ESP ; estabelece um novo base pointer",
            "  MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP",
            "  XOR ESI, ESI",
            "",
            "print_dec: ; empilha todos os digitos",
            "  MOV EDX, 0",
            "  MOV EBX, 0x000A",
            "  DIV EBX",
            "  ADD EDX, '0'",
            "  PUSH EDX",
            "  INC ESI ; contador de digitos",
            "  CMP EAX, 0",
            "  JZ print_next ; quando acabar pula",
            "  JMP print_dec",
            "",
            "print_next:",
            "  CMP ESI, 0",
            "  JZ print_exit ; quando acabar de imprimir",
            "  DEC ESI",
            "",
            "  MOV EAX, SYS_WRITE",
            "  MOV EBX, STDOUT",
            "",
            "  POP ECX",
            "  MOV [res], ECX",
            "  MOV ECX, res",
            "",
            "  MOV EDX, 1",
            "  INT 0x80",
            "  JMP print_next",
            "",
            "print_exit:",
            "  POP EBP",
            "  RET",
            "",
            "; subrotinas if/while",
            "binop_je:",
            "  JE binop_true",
            "  JMP binop_false",
            "",
            "binop_jg:",
            "  JG binop_true",
            "  JMP binop_false",
            "",
            "binop_jl:",
            "  JL binop_true",
            "  JMP binop_false",
            "",
            "binop_false:",
            "  MOV EBX, False",
            "  JMP binop_exit",
            "binop_true:",
            "  MOV EBX, True",
            "binop_exit:",
            "  RET",
            "",
            "_main:",
            "",
            "  PUSH EBP ; guarda o base pointer",
            "  MOV EBP, ESP ; estabelece um novo base pointer",
            ""
        ]

        footer = [
            "  ; interrupcao de saida",
            "  POP EBP",
            "  MOV EAX, 1",
            "  INT 0x80"
        ]

        # Escreve o cabeçalho e as instruções
        with open(filename, 'w') as f:
            for line in header:
                f.write(line + '\n')
            for instr in CodeGenerator.instructions:
                f.write(instr + '\n')
            for line in footer:
                f.write(line + '\n')


if __name__ == '__main__':

    arquivo = sys.argv[1]  # Arquivo de entrada

    # Lê o conteúdo do arquivo de entrada
    with open(arquivo, 'r') as file:
        operacao = file.read()

    # Gera a AST e avalia
    ast = Parser.run(operacao)
    symbol_table = SymbolTable()
    ast.Evaluate(symbol_table)

    # Remove a extensão do arquivo de entrada e adiciona '.asm'
    asm_filename = os.path.splitext(arquivo)[0] + ".asm"
    
    # Gera o arquivo .asm com o mesmo nome do arquivo de entrada
    CodeGenerator.write_to_file(asm_filename)

    print(f"Código Assembly gerado no arquivo '{asm_filename}'")


