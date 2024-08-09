import sys

def calcula(arg):
    #removendo os espaços
    arg = arg.replace(" ", "")
    arg_orginial = arg
    #pegando os sinais
    indice_mais = []
    indice_menos = []
    indice_sinais = []
    lista_sinais = []
    i = 0 
    while i in range(len(arg)):
        if arg[i] == "+":
            indice_mais.append(i)
            indice_sinais.append(i)
            lista_sinais.append("+")
            
        elif arg[i] == "-":
            indice_menos.append(i)
            indice_sinais.append(i)
            lista_sinais.append("-")

        i = i + 1

    arg = arg.replace("+", " ")
    arg = arg.replace("-", " ")
    lista_numeros = arg.split(" ")

    indice_numeros = []

    for j in range(len(lista_numeros) + len(indice_sinais)):
        if j not in indice_sinais:
            indice_numeros.append(j)

    primeiro_e_numero = False
       
    if indice_sinais[0] < indice_numeros[0]:
        primeiro_e_numero = False
    else:
        primeiro_e_numero = True

    primeiro_e_mais = True

    if indice_mais[0] < indice_menos[0]:
        primeiro_e_mais = True
        lista_sinais.insert(0, "+")
    else:
        primeiro_e_mais = False
        lista_sinais.insert(0, "-")

    primeiro_e_sinal = False

    if indice_sinais[0] < indice_numeros[0]:
        primeiro_e_sinal = True
    else:
        primeiro_e_sinal = False

    expressao = 0
    primeira_rodada = True

    for k in range (len(lista_numeros)):
        print(expressao)

        if lista_sinais[k] == "+":
            expressao = expressao + int(lista_numeros[k])
        else:
            expressao = expressao - int(lista_numeros[k])

             
    return expressao



if __name__ == '__main__':
    #pegando o argumento passado
    arg = sys.argv[1]
    print(f"argumento passado: {arg}")
    resultado = calcula(arg)
    print(f"resultado: {resultado}")