import sys

def calcula(arg):
    #removendo os espaços
    arg = arg.replace(" ", "")
    #pegando os dados dos sinais
    indice_mais = [] #indice de onde estão os sinais de mais'
    indice_menos = [] #indice de onde estão os sinais de menos
    indice_sinais = [] #indice de onde estão os sinais
    lista_sinais = [] #lista com os sinais

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

    #construindo a lista de números
    arg = arg.replace("+", " ")
    arg = arg.replace("-", " ")
    lista_numeros = arg.split(" ")

    #lista com os indices dos números
    indice_numeros = []

    for j in range(len(lista_numeros) + len(indice_sinais)):
        if j not in indice_sinais:
            indice_numeros.append(j)

    #checando se o primeiro elemento é um número ou um sinal
    primeiro_e_numero = False
       
    if indice_sinais[0] < indice_numeros[0]:
        primeiro_e_numero = False
    else:
        primeiro_e_numero = True
        lista_sinais.insert(0, "+")


    expressao = 0
    for k in range (len(lista_numeros)):

        if lista_sinais[k] == "+":
            expressao = expressao + int(lista_numeros[k])
        else:
            expressao = expressao - int(lista_numeros[k])

             
    return expressao



if __name__ == '__main__':
    #pegando o argumento passado
    arg = sys.argv[1]
    #print(f"argumento passado: {arg}")
    resultado = calcula(arg)
    print(resultado)