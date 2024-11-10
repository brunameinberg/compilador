import sys
import os
import re

FUNCTION_TYPE = "FUNCTION"


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
                raise Exception(f"Erro: Token inesperado: '{identifier}'")
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
        
        elif caractere == 'v':
            start = self.position
            while self.position < len(self.source) and self.source[self.position].isalpha():
                self.position += 1
            identifier = self.source[start:self.position]
            if identifier == 'void':
                self.current_token = Token("VOID_TYPE", identifier)
            else:
                raise Exception(f"Erro: Token inesperado: '{identifier}'")

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

            if identifier == 'scanf':
                self.current_token = Token("SCANF", identifier)
            elif identifier == 'printf':
                self.current_token = Token("PRINTF", identifier)
            elif identifier == 'return':
                self.current_token = Token("RETURN", identifier)
            elif identifier == 'if':
                self.current_token = Token("IF", identifier)
            elif identifier == 'else':
                self.current_token = Token("ELSE", identifier)
            elif identifier == 'while':
                self.current_token = Token("WHILE", identifier)
            elif identifier == 'int':
                self.current_token = Token("INT_TYPE", identifier)
            elif identifier == 'string' or identifier == 'str':
                self.current_token = Token("STRING_TYPE", identifier)
            elif identifier == 'bool':
                self.current_token = Token("BOOL_TYPE", identifier)
            else:
                # Caso não seja palavra reservada, é um identificador genérico
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

    def setter(self, identifier, value, var_type):
        if var_type != FUNCTION_TYPE and not isinstance(value, var_type):
            raise Exception(f"Erro: O valor '{value}' não corresponde ao tipo '{var_type.__name__}'")
        self.table[identifier] = (value, var_type)

    def check_type(self, identifier, expected_type):
        if identifier in self.table:
            _, stored_type = self.table[identifier]
            if stored_type != expected_type:
                raise Exception(f"Erro: Tipo incorreto. Esperado '{expected_type.__name__}', mas obtido '{stored_type.__name__}'")
        else:
            raise Exception(f"Erro: Identificador '{identifier}' não encontrado")


class Node:
    def __init__(self, value=None):
        self.value = value
        self.children = []

    def Evaluate(self, symbol_table):
        pass

class BinOp(Node):
    def __init__(self, value, left, right):
        if left is None or right is None:
            raise Exception(f"Erro ao criar BinOp: Operandos inválidos (left={left}, right={right})")
        super().__init__(value)
        self.children = [left, right]

    def Evaluate(self, symbol_table, global_symbol_table=None):
        left_value = self.children[0].Evaluate(symbol_table, global_symbol_table)
        right_value = self.children[1].Evaluate(symbol_table, global_symbol_table)

        if isinstance(left_value, bool):
            left_value = 1 if left_value else 0
        if isinstance(right_value, bool):
            right_value = 1 if right_value else 0

        if self.value == 'PLUS':

            if isinstance(left_value, str) or isinstance(right_value, str):
                return str(left_value) + str(right_value)

            return left_value + right_value
        
        elif self.value == 'MINUS':
            return left_value - right_value
        
        elif self.value == 'MULT':
            return left_value * right_value
        
        elif self.value == 'DIV':
            if right_value == 0:
                raise ValueError("Divisão por zero não permitida.")
            return left_value // right_value
        
        elif self.value == 'EQUALEQUAL':
            if type(left_value) != type(right_value):
                raise Exception(f"Erro: Comparação entre tipos incompatíveis '{type(left_value).__name__}' e '{type(right_value).__name__}'")
            return left_value == right_value
        
        elif self.value == 'LESS':
            if type(left_value) != type(right_value):
                raise Exception(f"Erro: Comparação entre tipos incompatíveis '{type(left_value).__name__}' e '{type(right_value).__name__}'")
            return left_value < right_value
        
        elif self.value == 'GREATER':
            if type(left_value) != type(right_value):
                raise Exception(f"Erro: Comparação entre tipos incompatíveis '{type(left_value).__name__}' e '{type(right_value).__name__}'")
            return left_value > right_value
        
        elif self.value == 'OR':
            return left_value or right_value
        
        elif self.value == 'AND':
            return left_value and right_value
        
        elif self.value == 'WHILE':
            while self.children[0].Evaluate(symbol_table, global_symbol_table):  # Verifica a condição
                self.children[1].Evaluate(symbol_table, global_symbol_table)  # Executa o bloco
            return 0  # Ao terminar o loop, retorna 0 ou algo neutro

        else:
            raise Exception(f"Operador desconhecido: {self.value}")

class UnOp(Node):
    def __init__(self, value, child):
        super().__init__(value)
        self.children = [child]

    def Evaluate(self, symbol_table, global_symbol_table=None):
        child_value = self.children[0].Evaluate(symbol_table, global_symbol_table)

        if self.value == 'PLUS':
            return child_value
        
        elif self.value == 'MINUS':
            return -child_value
        
        elif self.value == 'NOT':
            if not isinstance(child_value, (int, bool)):
                raise Exception(f"Erro: Operador '!' não pode ser aplicado ao tipo '{type(child_value).__name__}'")
            return not child_value

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self, symbol_table, global_symbol_table=None):
        return self.value

class NoOp(Node):
    def Evaluate(self, symbol_table, global_symbol_table=None):
        return 0

class Identifier(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self, symbol_table, global_symbol_table=None):
        value, _ = symbol_table.getter(self.value)  # Extrai apenas o valor da tupla
        return value
    
class Assignment(Node):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def Evaluate(self, symbol_table, global_symbol_table=None):
        value = self.expression.Evaluate(symbol_table)
        _, var_type = symbol_table.getter(self.identifier.value)
        symbol_table.setter(self.identifier.value, value, var_type)

class Print(Node):
    def __init__(self, expression):
        self.expression = expression

    def Evaluate(self, symbol_table, global_symbol_table=None):
        value = self.expression.Evaluate(symbol_table, global_symbol_table)

        if isinstance(value, bool):
            value = int(value)
        
        print(f"{value}")

class Statements(Node):
    def __init__(self):
        self.statements = []

    def Evaluate(self, symbol_table, global_symbol_table=None):

        if global_symbol_table is None:
            global_symbol_table = symbol_table

        #print("[DEBUG] Executando bloco de statements...")
        #print(f"[DEBUG] Tabela de símbolos global no início: {global_symbol_table.table}")
        #print(f"[DEBUG] Tabela de símbolos local no início: {symbol_table.table}")


        # Primeiro, registra todas as funções na tabela de símbolos
        for statement in self.statements:
            if isinstance(statement, FuncDec):
                statement.Evaluate(global_symbol_table)
                #print(f"Função '{statement.func_name.value}' registrada com sucesso.")

        # Em seguida, executa o restante do programa
        for statement in self.statements:
            #print(f"Executando statement: {statement}")
            if not isinstance(statement, FuncDec):
                result = statement.Evaluate(symbol_table, global_symbol_table)
                if isinstance(statement, Return):  # Detecta um nó de retorno
                    return result  # Propaga o valor de retorno
        return None

class If(Node):
    def __init__(self, condition, if_block, else_block=None):
        super().__init__('IF')
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block

    def Evaluate(self, symbol_table,  global_symbol_table=None):
        if self.condition.Evaluate(symbol_table):  
            return self.if_block.Evaluate(symbol_table, global_symbol_table)
        elif self.else_block:  
            return self.else_block.Evaluate(symbol_table, global_symbol_table)
        return 0  

class VarDec(Node):
    def __init__(self, var_type, identifiers, expressions=None):
        super().__init__()
        self.var_type = var_type
        self.identifiers = identifiers
        self.expressions = expressions or []

    def Evaluate(self, symbol_table, global_symbol_table=None):
        for i, identifier in enumerate(self.identifiers):
            if identifier.value in symbol_table.table:
                raise Exception(f"Erro: Variável '{identifier.value}' já foi declarada")
            
            # Verificar se há expressão associada
            if i < len(self.expressions) and self.expressions[i] is not None:
                value = self.expressions[i].Evaluate(symbol_table, global_symbol_table)
                if not isinstance(value, self.var_type):
                    raise Exception(f"Erro: Tipo incompatível para '{identifier.value}'")
                symbol_table.setter(identifier.value, value, self.var_type)
            else:
                if self.var_type == int:
                    initial_value = 0
                elif self.var_type == str:
                    initial_value = ""  # Corrigido para string vazia ao invés de None
                elif self.var_type == bool:
                    initial_value = False
                else:
                    raise Exception(f"Erro: Tipo de dado desconhecido para inicialização")
                
                symbol_table.setter(identifier.value, initial_value, self.var_type)

class StringVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self, symbol_table, global_symbol_table=None):
        return self.value
    
class FuncDec(Node):
    def __init__(self, func_name, var_dec, statements, return_type):
        super().__init__('FUNCDEC')
        self.func_name = func_name  
        self.var_dec = var_dec      
        self.statements = statements  
        self.return_type = return_type

    def Evaluate(self, global_symbol_table):

        #print(f"Registrando função '{self.func_name.value}' na tabela de símbolos.")
        global_symbol_table.setter(self.func_name.value, self, FUNCTION_TYPE)
        #print(f"Tabela de símbolos global após registro: {global_symbol_table.table}")

   

class FuncCall(Node):
    def __init__(self, func_name, args):
        super().__init__('FUNCCALL')
        self.func_name = func_name  
        self.args = args           

    def Evaluate(self, symbol_table, global_symbol_table=None):

        #print(f"[DEBUG] Chamando função '{self.func_name.value}'")
        #print(f"[DEBUG] Tabela de símbolos global: {global_symbol_table.table}")
        #print(f"[DEBUG] Tabela de símbolos local: {symbol_table.table}")


        # Permitir a passagem da tabela global como argumento
        if global_symbol_table is None:
            global_symbol_table = symbol_table

        #print(f"Tentando chamar a função '{self.func_name.value}'")
        #print(f"Tabela de símbolos global antes da chamada: {global_symbol_table.table}")

        # Acessa a função na tabela de símbolos global
        if self.func_name.value not in global_symbol_table.table:
            raise Exception(f"Erro: Função '{self.func_name.value}' não declarada.")

        func_dec, func_type = global_symbol_table.getter(self.func_name.value)

        if func_type != FUNCTION_TYPE:
            raise Exception(f"Erro: '{self.func_name.value}' não é uma função.")
        
        #print(f"Chamada válida para '{self.func_name.value}'. Avaliando argumentos...")

        # Criar uma tabela local para a função
        local_symbol_table = SymbolTable()

        if len(self.args) != len(func_dec.var_dec.identifiers):
            raise Exception(f"Erro: Número incorreto de argumentos para função '{self.func_name.value}'.")

        # Insere argumentos na tabela local
        for i, arg in enumerate(self.args):
            arg_value = arg.Evaluate(symbol_table)
            param_identifier = func_dec.var_dec.identifiers[i]
            local_symbol_table.setter(param_identifier.value, arg_value, func_dec.var_dec.var_type)
            #print(f"Argumento '{param_identifier.value}' definido como {arg_value}.")

        #print(f"Tabela local da função '{self.func_name.value}': {local_symbol_table.table}")
        result = func_dec.statements.Evaluate(local_symbol_table, global_symbol_table)

        if result is None and func_dec.return_type != 'VOID_TYPE':
            raise Exception(f"Erro: A função '{self.func_name.value}' não possui um retorno explícito.")

        #print(f"Função '{self.func_name.value}' retornou: {result}")
        return result

class Return(Node):
    def __init__(self, expression):
        self.expression = expression

    def Evaluate(self, symbol_table, global_symbol_table=None):
        if global_symbol_table:
            func_dec, _ = global_symbol_table.getter(self.func_name.value)
            if func_dec.return_type == 'VOID_TYPE' and self.expression is not None:
                raise Exception(f"Erro: Função '{self.func_name.value}' do tipo 'void' não pode retornar valores.")

        return self.expression.Evaluate(symbol_table, global_symbol_table)


class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer 

    def parseProgram(self):
        statements = Statements()  # Criação do nó raiz para armazenar funções
        while self.tokenizer.current_token.type != 'EOF':  # Permitir várias funções no programa
            statements.statements.append(self.parseFunction())  # Adicionar cada função

        # Adiciona a chamada para a função 'main' como último filho
        main_call = FuncCall(Identifier("main"), [])
        statements.statements.append(main_call)

        return statements
    
    def parseFunction(self):

        if self.tokenizer.current_token.type not in ['INT_TYPE', 'VOID_TYPE']:
            raise Exception("Erro: Esperado 'int' ou 'void' no início da função")

        
        return_type = self.tokenizer.current_token.type

        self.tokenizer.selectNext()  

        if self.tokenizer.current_token.type != 'IDENT':
            raise Exception("Erro: Esperado nome da função após 'int'")
        
        func_name = Identifier(self.tokenizer.current_token.value)
        self.tokenizer.selectNext()  

        if self.tokenizer.current_token.type != 'EPARENT':
            raise Exception("Erro: Esperado '(' após nome da função")
        
        self.tokenizer.selectNext()  
        
        parameters = []  # Lista de identificadores
        if self.tokenizer.current_token.type != 'DPARENT':  # Verifica se há parâmetros
            while True:
                if self.tokenizer.current_token.type != 'INT_TYPE':
                    raise Exception("Erro: Esperado tipo de parâmetro (int)")

                self.tokenizer.selectNext()

                if self.tokenizer.current_token.type != 'IDENT':
                    raise Exception("Erro: Esperado nome do parâmetro")

                param_name = Identifier(self.tokenizer.current_token.value)
                parameters.append(param_name)
                self.tokenizer.selectNext()

                if self.tokenizer.current_token.type == 'COMMA':
                    self.tokenizer.selectNext()  # Continua lendo outros parâmetros
                elif self.tokenizer.current_token.type == 'DPARENT':
                    break
                else:
                    raise Exception("Erro: Esperado ',' ou ')' após parâmetro")

        self.tokenizer.selectNext()  # Consome o ')'

        # Lê o bloco de declarações e statements
        statements = self.parseBlock()

        return FuncDec(func_name, VarDec(int, parameters), statements, return_type)

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
            if self.tokenizer.current_token.type == 'EQUAL':
                self.tokenizer.selectNext()
                expr = self.parseRelational()
            if self.tokenizer.current_token.type == 'SEMICOLON':
                self.tokenizer.selectNext()
                return Assignment(identifier, expr)
            if self.tokenizer.current_token.type == 'EPARENT':
                self.tokenizer.selectNext()
                args = []
                while self.tokenizer.current_token.type != 'DPARENT':
                    args.append(self.parseRelational())
                    if self.tokenizer.current_token.type == 'COMMA':
                        self.tokenizer.selectNext()
                self.tokenizer.selectNext()
                return FuncCall(identifier, args)
        
        elif self.tokenizer.current_token.type == "RETURN":
            self.tokenizer.selectNext()
            expr = self.parseRelational()
            if self.tokenizer.current_token.type != 'SEMICOLON':
                raise Exception("Erro: Esperado ';' após 'return'")
            self.tokenizer.selectNext()
            return Return(expr)
        
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
            right = self.parseTerm()
            if result is None or right is None:
                raise Exception(f"Erro: Operação de expressão inválida (left={result}, right={right})")
            result = BinOp(op, result, right)
        return result


    def parseTerm(self):
        result = self.parseFactor()
        while self.tokenizer.current_token.type == "MULT" or self.tokenizer.current_token.type == "DIV" or self.tokenizer.current_token.type == "AND":
            op = self.tokenizer.current_token.type 
            self.tokenizer.selectNext()

            right = self.parseFactor()
            if result is None or right is None:
                raise Exception(f"Erro: Operação de termo inválida (left={result}, right={right})")
            result = BinOp(op, result, right)
        return result

    def parseFactor(self):

        if self.tokenizer.current_token.type == 'NUMBER':
            result = IntVal(self.tokenizer.current_token.value)
            self.tokenizer.selectNext()
            return result
        
        elif self.tokenizer.current_token.type == 'IDENT':
            identifier = Identifier(self.tokenizer.current_token.value)
            self.tokenizer.selectNext()
            if self.tokenizer.current_token.type == 'EPARENT':  # Chamada de função
                self.tokenizer.selectNext()
                args = []
                while self.tokenizer.current_token.type != 'DPARENT':
                    args.append(self.parseRelational())
                    if self.tokenizer.current_token.type == 'COMMA':
                        self.tokenizer.selectNext()
                self.tokenizer.selectNext()
                return FuncCall(identifier, args)
            return identifier
           
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
        
        elif self.tokenizer.current_token.type == 'SCANF':
            self.tokenizer.selectNext()
            if self.tokenizer.current_token.type != 'EPARENT':
                raise Exception("Erro: Esperado '(' após 'scanf'")
            self.tokenizer.selectNext()
            if self.tokenizer.current_token.type != 'DPARENT':
                raise Exception("Erro: Esperado ')' após 'scanf'")
            self.tokenizer.selectNext()
            return IntVal(int(input()))
        
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
            right = self.parseExpression()
            if result is None or right is None:
                raise Exception(f"Erro: Operação relacional inválida (left={result}, right={right})")
            return BinOp(op, result, right)
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

if __name__ == '__main__':

    arquivo = sys.argv[1]

    with open(arquivo, 'r') as file:
        operacao = file.read()

    ast = Parser.run(operacao)
    global_symbol_table = SymbolTable()
    #print("Executando AST...")
    ast.Evaluate(global_symbol_table)

    #print("Tabela de símbolos global final:")
    #print(global_symbol_table.table)
