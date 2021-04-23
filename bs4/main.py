import bs4
import requests
import requests_cache
import re

requests_cache.install_cache('banco')

def exibir_caracteres(palavra, palavra_chave):

    if (len(palavra) != 0):
        palavra =  str(palavra[0])
        index = palavra.find(palavra_chave)
        inicio = index
        fim = index + len(palavra_chave) -1
        resultado_inicial = ""
        resultado_final = ""
        count = 0
        while (inicio != 0 and count <= 15 ) :
            inicio -= 1
            resultado_inicial = palavra[inicio] + resultado_inicial
            count += 1
        count = 0
        while ( (fim < len(palavra)) and count <= 15 ):
            fim += 1
            resultado_final += palavra[fim]
            count += 1
        return resultado_inicial + "(" + palavra_chave + ")" + resultado_final
    else:
        return "Palavra não encontrada"


#pagina = input("Digite o link da página a ser carregada: ")
pagina = "https://conexaopolitica.com.br/"
response = requests.get(pagina)

continuar = 1

if (response.status_code == 200):

    while continuar:

        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        links = soup.select('a[href^="http"]',limit = 10)

        print("\nTítulos\n")
        for j in range(len(links)):
            print("{0} - {1} - {2}".format((j+1),links[j].text,links[j].attrs['href']))

        titulo = int(input("Digite o número do título: ")) - 1
        palavra_chave = input("Digite uma palavra-chave: ")

        print("Selecionado : {0}\n".format( links[titulo]))
        pagina = links[titulo].attrs['href']


        pagina_escolhida_response = requests.get(pagina)

        if (pagina_escolhida_response.status_code == 200):
            soup_pagina_escolhida = bs4.BeautifulSoup(pagina_escolhida_response.text, 'html.parser')
            encontrar_palavra_chave = soup_pagina_escolhida.find_all(string=re.compile(palavra_chave))
            print(exibir_caracteres(encontrar_palavra_chave,palavra_chave))
        else:
            print("Erro "+str(pagina_escolhida_response.status_code)+" ao acessar o link selecionado")
        continuar = int(input("\nDeseja continuar (1-SIM / 0-NÃO)?: "))


else:
    print("Erro ",response.status_code)



