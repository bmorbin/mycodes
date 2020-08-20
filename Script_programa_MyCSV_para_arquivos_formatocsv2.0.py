"""
Created on Tue Aug 18 15:37:07 2020

@author: Bruno
"""

# -*- coding: utf-8 -*-
BARRA_SEPARADORA = "___________________________________________________________________________________________________________"
"""
Script que lerá informações e colocará no formato CSV (.csv)
Ideia: Programa que facilitará armazenar informações sobre ganhos e perdas monetárias pessoal
"""
import csv     #Biblioteca padrão utilizada para trabalhar no formato CSV
#import os.path#Biblioteca responsável por verificar se o arquivo digitado no passo #0.1 é novo ou não 
               #(acessar:<https://www.it-swarm.dev/pt/python/como-faco-para-verificar-se-existe-um-arquivo-sem-excecoes/957389119/>). Obs.: A biblioteca "os" contém a "os.path": Fonte<https://www.it-swarm.dev/pt/python/devo-usar-import-os.path-ou-import-os/969997168/>
import os      #Biblioteca responsável por remover o arquivo para depois criá-lo com o cabeçalho atualizado no passo #0.2
               #Fonte: <https://thispointer.com/python-how-to-insert-lines-at-the-top-of-a-file/> 
import shutil  #Biblioteca que utiliza a "os" e facilita para mover arquivo de uma pasta para outra
               #Fonte: <https://codare.aurelio.net/2006/10/03/python-mover-arquivo-para-outro-diretorio/>

#Função principal de introdução e encerramento do programa
def main():
    
    print(BARRA_SEPARADORA)
    print()
    print("MyCSV Program - Created by Bruno Groper Morbin®\nVersão NãoExcel")
    print(BARRA_SEPARADORA)
    print()
    print('ESTE PROGRAMA TEM POR FINALIDADE CRIAR, CARREGAR E ATUALIZAR UMA PLANILHA CUJO FORMATO DO ARQUIVO É ".csv".')
    print('\nATENÇÃO: Não utilizar este programa para editar planilhas do Excel. Neste caso, utilizar a Versão Excel.\n         Não usar o caractere "," em nenhum momento.\n'+BARRA_SEPARADORA+'\n\n*Nota(1): Caso queira acessar uma planilha já existente, é necessário que a mesma não esteja aberta.')
    print('*Nota(2): Caso precise visualizar a planilha, ir para o site do Google Planilhas, depois seguir os seguintes \npassos: Iniciar uma nova planilha "em branco" -> "Arquivo" -> "Importar" -> Selecionar arquivo ".csv" presen-\nte no mesmo diretório que esse programa -> Em "Converter texto em números, datas e fórmulas", selecionar \n"Não" -> "Importar dados".')
    print('Para salvar a planilha após visualizada, ir em "Arquivo" -> "Fazer download" -> "Valores separados por vírgu-\nla (.csv, página atual)" -> Mover esse arquivo da pasta de Downloads para a pasta que contém esse programa \n-> Alterar o nome do arquivo para o nome original (antes da visualização).')
    print('\nObservação: Para acessar as planilhas criadas e acessadas por esse programa, ir para a pasta "Planilhas-\nMyCSV(NaoExcel)" localizada no disco local.')
    print(BARRA_SEPARADORA)
    
    print('\n')
    escolha0 = input('Deseja acessar a planilha padrão "MyPlan.csv" com o cabeçalho pronto?(S/N): ').strip()
    print()
    
    executa(escolha0)
    
    
    parada = False
    while parada == False:
        print(BARRA_SEPARADORA+'\n')
        escolha3 = input("Quer ATUALIZAR/CRIAR outra planilha?(S/N): ").strip()
        if escolha3 != '' and escolha3 in 'SimsimSIM': executa()
        else: print('\nFECHANDO O PROGRAMA...'); parada = True
            
#---
#0: Função que adiciona informações para uma planilha nova ou não (pode ser criada a partir daqui).
def executa(escolha0='n'): #caso não seja dado parâmetro, a função entenderá escolha0 com atribuição 'n'
    '''(string) -> NoneType
    RECEBE string referente à escolha do indivíduo em relação a pergunta inicial do programa (se o mesmo quer acessar a planilha padrão ou não)
    RETORNA None
    '''    
    #---
    #0.1: Perguntar nome do arquivo que deseja atualizar ou criar
    
    #Fonte: <https://www.it-swarm.dev/pt/python/como-obter-o-caminho-completo-do-diretorio-do-arquivo-atual-no-python/969063816/>
    #Pegar o diretório que está programa e extrair somente os primeiros dois caracteres do disco local, por exemplo "C:"
    dire_ori = os.path.dirname(__file__)
    dire = disc_rig(dire_ori)
    
    if escolha0 =="": return None
    else:    
        if escolha0 in "SimsimSIM":
            print()
            nome_arq = 'MyPlan.csv' #Nome do arquivo que deve estar na pasta "Planilhas-MyCSV(NaoExcel)" no disco local
            if not os.path.isfile(dire+"/Planilhas-MyCSV(NãoExcel)/Myplan.csv"): 
                #Fonte: <https://pt.stackoverflow.com/questions/170615/como-criar-um-diret%C3%B3rio-em-python> 
                #Criando um diratório com a pasta "Planilhas-MyCSV(NaoExcel)"
                os.makedirs(dire + "/Planilhas-MyCSV(NãoExcel)")
                
                #Movendo MyPlan.csv da pasta em que foi feita o download (ou que contém o programa executável) para a pasta "Planilhas-MyCSV" semi-criada no disco local
                shutil.move("MyPlan.csv",dire + "/Planilhas-MyCSV(NãoExcel)")
        else:
            print(BARRA_SEPARADORA)
            print('\n')
            nome_arq = input("-> Digite o nome do arquivo (p/ atualizar ou criar): ").strip()
            print()
            
            if not os.path.isfile("C:/Planilhas-MyCSV(NãoExcel)/MyPlan.csv"):
                #Criando um diratório com a pasta Planilhas-MyCSV
                os.makedirs(dire + "/Planilhas-MyCSV(NãoExcel)")
            
            #implementar formato CSV caso o indivíduo não tenha explicitado acima
            if nome_arq == "":
                return None
            else:
                if '.csv' not in nome_arq:
                    nome_arq += '.csv'

    #---
    #0.2: escrever diretório da planilha para ver se ela já existe ou não no passo #0.3
    
    path = dire + '/Planilhas-MyCSV(NãoExcel)/' + nome_arq

            
    #---
    #0.3: criar colunas com seus respectivos títulos, ou incrementá-la com mais algum (ou alguns) título(s)
    
    #verifica se o arquivo já é existente ou não. Obs.: verifica se a planilha já existe na pasta "Planilhas-MyCSV(NaoExcel)" e somente nelas.
    if os.path.isfile(path):
        cabecalho = ""
        parada = False #bandeira inicialmente levantada 
        while parada == False:
            escolha1 = input('Deseja adicionar uma nova coluna para a sua planilha "{}"?(S/N): '.format(nome_arq)).strip()
            if escolha1 != "" and escolha1 in "SimsimSIM":
                new_column = input('-> Nomeie sua nova coluna (Obs.: não usar caractere ","): ').strip()
                print()
                if new_column != "": #condição que verifica se a pessoa não colocou nome na nova coluna 
                    cabecalho += "," + new_column #";" será usado como delimitador do arquivo CSV
            else:
                parada = True #bandeira abaixada (sair do while)
        cabecalho += "\n"
        atualize_cab(cabecalho,path) #função para adicionar os novos títulos ao cabeçalho da planilha já existente
        cabecalho = read_columns(path)
        
    else:
        cabecalho = []
        num_columns = int(input("-> Quantas colunas de cabeçalho você irá criar?: ").strip())
        for i in range(1 , num_columns+1):
            new_column = input("   -> Nomeie a {}ª coluna: ".format(i)).strip()
            cabecalho += [new_column]
        adc_in_excel(cabecalho, path)
        
    #---
    #2: mensagens para o indivíduo adicionar novas informações em cada coluna
    #   atentar-se aos casos em que a informação for nula(vazia) em uma determinada coluna
    
    print()
    print("Digite todas novas informações a seguir")
    lst_infosordered = [] #lista com todas informções que serão adicionadas na ordem
    for titulo in cabecalho:
        info = input("-> {}: ".format(titulo)).strip()
        lst_infosordered += [info]
    adc_in_excel(lst_infosordered,path)
    
    parada = False
    while parada == False:        
        print()
        escolha2 = input("Deseja adicionar novas informações?(S/N): ").strip()
        if escolha2 != "" and escolha2 in "SimsimSIM":
            adc_infos(cabecalho,path)
        else:
            print()
            parada = True

#---
#1: ler 1ª coluna, referente ao que se trata cada coluna (usado para o passo #0.1)

def read_columns(path):
    '''(string) -> list
    RECEBE string referente ao caminho do arquivo que contém a planilha no formato CSV
    RETORNA lista com o título de cada coluna como elementos
    '''
    #para ler apenas uma linha, usei essa fonte de pesquisa:<https://stackoverflow.com/questions/27264818/dont-understand-pythons-csv-reader-object>
    with open(path,'r') as planilha:
        leitura = csv.reader(planilha,delimiter=',')
        #Fonte: <https://www.w3schools.com/python/ref_func_next.asp> para entender a sintaxe da function next()
        #       caso a planilha já exista, porém está sem cabeçalho, a função read_columns retorna [] como default.
        return next(leitura, [])
       
#---
#3: função que pegará as informações e implementará-las no arquivo EXCEL     

def adc_in_excel(lst_infosordered,path):
    '''(list,string) -> NoneType
    RECEBE lista referente às novas informações a implementar e nome do caminho do arquivo para modificar
    RETORNA None
    '''
    #Fonte: <https://medium.com/@renatojlelis/opera%C3%A7%C3%B5es-em-arquivos-csv-com-python-1aee99273fd5>
    #       <https://www.it-swarm.dev/pt/python/acrescentar-nova-linha-ao-antigo-arquivo-csv-python/968000475/> #utilizado, pois "a" trocado por "w" faz com que o arquivo seja modificado
    with open(path,'a',newline='') as planilha:
        adc_line = csv.writer(planilha , delimiter = ",") #delimitador identificado no Excel
        adc_line.writerow(lst_infosordered)

#---
#4: função que repete os passos de adicionar novas informações

def adc_infos(cabecalho,path):
    '''(list,string) -> NoneType
    RECEBE lista com títulos do cabeçalho e nome do arquivo que contém a planilha para atualizá-la
    RETORNA None
    '''
    print()
    print("Digite todas novas informações a seguir")
    lst_infosordered = [] #lista com todas informções que serão adicionadas na ordem
    for titulo in cabecalho:
        info = input("-> {}: ".format(titulo)).strip()
        lst_infosordered += [info]
    adc_in_excel(lst_infosordered,path)
    
#---
#5: função executável apenas se a condição do passo #0.1 for verdadeira, ou seja, apenas se a planilha já existir e o indivíduo desejar adicionar novos títulos ao cabeçalho (novas colunas)
def atualize_cab(adc,path):
    '''(string,string) -> NoneType
    RECEBE string referente ao(s) novo(s) título(s) de cabeçalho adiciono(s) e outra string referente ao nome do arquivo 
    RETORNA None
    '''    
    with open(path,'r') as arq_r:
        leitura = csv.reader(arq_r , delimiter=';') #a partir deste delimitador, a função identifica a separação dos valores em cada célula do arquivo CSV
        new_doc="" #criado um novo documento que conterá o cabeçalho atualizado
        for linha in leitura:
            if len(linha) > 0: #condição necessária para ver se a linha é vazia ou não
                new_doc += linha[0] + adc
            else:
                new_doc += adc
            adc="\n" 
        
    os.remove(path) #removendo a planilha antiga para adicionar a nova atualizada
        
    with open(path,'a',newline='') as arq_w:
        a = new_doc.split('\n')
        escrita = csv.writer(arq_w , delimiter=',')
        for linha in a[:-1]: #como '\n' foi usado para separar as linha em "new_doc", portanto foi preciso colocar esse intervalo ([:-1]) para não considerar o último elemento da lista "a" que é uma string vazia
            linha = linha.split(',')
            escrita.writerow(linha)

#---
#6: Função que identifica o disco rígido local do computador em que está sendo usado este programa
def disc_rig(dire_ori):
    '''(string) -> string
    RECEBE string referente ao caminho em que este programa está sendo executado
    RETORNA string referente aos primeiros caracteres antes da priimeira barra ("/") para identificar o disco local do sistema operacional do indivíduo
    '''
    dire = "" #No caso de sistema operacional como Linux, o disco rígido é simplesmente "/". Fonte:<https://gizmodo.uol.com.br/disco-rigido-c/>
    for char in dire_ori:
        if char in "/\\" : return dire
        else: dire += char
    return dire

#---
if __name__ == "__main__":
    main()







