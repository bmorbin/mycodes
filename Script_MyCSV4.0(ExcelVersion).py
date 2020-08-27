# -*- coding: utf-8 -*-
BARRA_SEPARADORA = "___________________________________________________________________________________________________________"
BARRA_SEPARADORA2 = '==========================================================================================================='
"""
Script que lerá informações e colocará numa tabela do EXCEL (formato .CSV).
Ideia: Programa que facilitará armazenar informações sobre ganhos e perdas monetárias pessoais.
"""
import csv     #Biblioteca padrão utilizada para trabalhar com o formato CSV.
#import os.path#Biblioteca responsável por verificar se o arquivo digitado no passo #0.1 é novo ou não; 
               #(acessar:<https://www.it-swarm.dev/pt/python/como-faco-para-verificar-se-existe-um-arquivo-sem-excecoes/957389119/>). Obs.: A biblioteca "os" contém a "os.path": Fonte<https://www.it-swarm.dev/pt/python/devo-usar-import-os.path-ou-import-os/969997168/>
import os      #Biblioteca responsável por remover o arquivo para depois criá-lo com o cabeçalho atualizado no passo #0.2;
               #Fonte: <https://thispointer.com/python-how-to-insert-lines-at-the-top-of-a-file/> 
#import shutil #Biblioteca que utiliza a biblioteca "os" e facilita para mover arquivo de uma pasta para outra;
               #Fonte: <https://codare.aurelio.net/2006/10/03/python-mover-arquivo-para-outro-diretorio/>

#---
#Função principal de introdução e encerramento do programa
def main():
    
    print(BARRA_SEPARADORA)
    print()
    print("MyCSV Program - Created by Bruno Groper Morbin®\nVersão para Excel")
    print(BARRA_SEPARADORA)
    print()
    print('ESTE PROGRAMA TEM POR FINALIDADE CRIAR OU ATUALIZAR UMA PLANILHA CUJO FORMATO DO ARQUIVO É ".csv".\n\nObservação: Caso queira acessar uma planilha já existente, é necessário que a mesma não esteja aberta durante a \nexecução do programa.')
    print('Nota: Esta versão possibilita criar e editar planilhas e depois acessá-las no Excel. Não é recomendá-\nvel abrir os arquivos deste programa em outro aplicativo que não seja o Excel (capaz de perder toda planilha).')
    print('\nATENÇÃO: Não usar o caractere ";" em nenhum momento. Não mover a planilha da pasta "Planilhas-MyCSV(Excel)"" \npara outra!')
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
def executa(escolha0='n'): #caso não seja dado parâmetro, a função entenderá escolha0 com atribuição "n"(não).
    '''(string) -> NoneType
    RECEBE string referente à escolha do indivíduo em relação a pergunta inicial do programa (se o mesmo quer acessar a planilha padrão ou não).
    RETORNA None.
    '''    
    #---
    #0.1: Perguntar nome do arquivo que deseja atualizar ou criar.
    
    #Fonte: <https://www.it-swarm.dev/pt/python/como-obter-o-caminho-completo-do-diretorio-do-arquivo-atual-no-python/969063816/>
    #Pegar o diretório que está programa e extrair somente os primeiros dois caracteres do disco local, por exemplo "C:".
    dire_ori = os.path.dirname(__file__)
    dire = disc_rig(dire_ori)
    
    if escolha0 =="": return None
    else:    
        if escolha0 in "SimsimSIM":
            print()
            nome_arq = 'MyPlan.csv' #Nome do arquivo que deve estar na pasta "Planilhas-MyCSV" no disco local
            if not os.path.isfile(dire+"/Planilhas-MyCSV(Excel)/Myplan.csv"): 
                #Fonte: <https://pt.stackoverflow.com/questions/170615/como-criar-um-diret%C3%B3rio-em-python> 
                #Criando um diratório com a pasta Planilhas-MyCSV
                os.makedirs(dire + "/Planilhas-MyCSV(Excel)")
                
                #Criando a planilha "MyPlan" com as seguintes colunas:
                with open(dire+"/Planilhas-MyCSV(Excel)/Myplan.csv",'a',newline="") as plan:
                    escrita = csv.writer(plan,delimiter = ";")
                    escrita.writerow(['Data(dd/mm/aaaa). Obs.: colocar data do vencimento caso o pagamento foi feito por crédito','Ganhei(valor em R$)','Paguei/Gastei(valor em R$)',\
                                      'Parcelas(em x meses sendo x um número interio)','Troco/Sobrou(valor em R$)','Trabalho feito(descrição)','Compra/Pagamento feito(descrição)','Categoria da compra/pagamento(p. ex.: Alimento ou Conta de luz etc.)',\
                                          'Tipo de pagamento(p. ex.: Crédito ou Débito etc.)'])
                #Criando a opção de colocar saldo atual a ser considerado nas análises do relatório:
                SALDO = round(float(input("Primeira vez acessando a planilha MyPlan?\nDigite seu saldo atual para ser considerado no relatório financeiro (valor em R$): ").strip()),2)
                with open(dire+"/Planilhas-MyCSV(Excel)/SALDO-MyPlan.csv",'a',newline="") as saldo:
                    escrita = csv.writer(saldo,delimiter=";")
                    escrita.writerow([SALDO])
                '''
                #Código abaixo para caso quisesse mandar a planilha já pronta e movê-la para a pasta correta.
                
                #Movendo MyPlan.csv da pasta em que foi feita o download (ou que contém o programa executável) para a pasta "Planilhas-MyCSV" semi-criada no disco local
                shutil.move("MyPlan.csv",dire + "/Planilhas-MyCSV(Excel)")
                '''
        else:
            print(BARRA_SEPARADORA)
            print('\n')
            nome_arq = input("-> Digite o nome do arquivo (p/ atualizar ou criar): ").strip()
            print()
            
            if not os.path.isfile("C:/Planilhas-MyCSV(Excel)/MyPlan.csv"):
                #Criando um diratório com a pasta Planilhas-MyCSV
                os.makedirs(dire + "/Planilhas-MyCSV(Excel)")
                
            #implementar formato CSV caso o indivíduo não tenha explicitado acima
            if nome_arq == "":
                return None
            else:
                if '.csv' not in nome_arq:
                    nome_arq += '.csv'
        
    #---
    #0.2: escrever diretório da planilha para ver se ela já existe ou não no passo #0.3
    
    path = dire + '/Planilhas-MyCSV(Excel)/' + nome_arq
    
    #---
    #0.3: criar colunas com seus respectivos títulos, ou incrementá-la com mais algum (ou alguns) título(s)
    
    #verifica se o arquivo já é existente ou não. Obs.: verifica se a planilha já existe na pasta "Planilhas-MyCSV" e somente nelas.
    if os.path.isfile(path):
        cabecalho = ""
        parada = False #bandeira inicialmente levantada 
        while parada == False:
            escolha1 = input('Deseja adicionar uma nova coluna para a sua planilha "{}"?(S/N): '.format(nome_arq)).strip()
            if escolha1 != "" and escolha1 in "SimsimSIM":
                new_column = input('-> Nomeie sua nova coluna (Obs.: não usar caractere ";" nem ",". Substituir esses caracteres por "."): ').strip()
                print()
                if new_column != "": #condição que verifica se a pessoa não colocou nome na nova coluna 
                    cabecalho += ";" + new_column #";" será usado como delimitador do arquivo CSV
            else:
                print()
                parada = True #bandeira abaixada (sair do while)
        cabecalho += "\n"
        atualize_cab(cabecalho,path) #função para adicionar os novos títulos ao cabeçalho da planilha já existente
        cabecalho = read_columns(path)
        
    else:
        cabecalho = []
        num_columns = int(input("-> Quantas colunas de cabeçalho você irá criar?: ").strip())
        for i in range(1 , num_columns+1):
            new_column = input('   -> Nomeie a {}ª coluna (Obs.: não usar caractere ";" nem ",". Substituir esses caracteres por "."): '.format(i)).strip()
            cabecalho += [new_column]
        adc_in_excel([cabecalho], path)
    
    columns = ""
    for column in cabecalho:
        columns += "   |" + column[:10]+'...' 
    print('\nAs colunas presentes no seu cabeçalho são estas:\n'+columns+'\n\n')
    
    #---
    #2: mensagens para o indivíduo adicionar novas informações em cada coluna
    #   atentar-se aos casos em que a informação for nula(vazia) em uma determinada coluna
    
    print(BARRA_SEPARADORA2)
    print('Digite todas novas informações a seguir\nAPERTE ENTER CASO NÃO TENHA A INFORMAÇÃO DE DETERMINADA COLUNA\nUSE "." no lugar da "," ou no lugar de ";"!\n')
    lst_infosordered = [] #lista com todas informações que serão adicionadas na ordem
    cate_myplan = False
    pagamento_myplan = False
    uso_myplan = False
    for titulo in cabecalho:
        if titulo == "Categoria da compra/pagamento(p. ex.: Alimento ou Conta de luz etc.)" and nome_arq in ["MyPlan.csv","Myplan.csv","MYPLAN.csv","myplan.csv","myPlan.csv"]:
            cate_myplan = True
            uso_myplan = True
            if os.path.isfile(dire + "/Planilhas-MyCSV(Excel)/Categorias-MyPlan.txt"):
                with open(dire + "/Planilhas-MyCSV(Excel)/Categorias-MyPlan.txt","r") as text_r:
                    print('\nAs Categorias já utilizadas na planilha foram:\n' + text_r.read())
                    
        elif titulo == "Tipo de pagamento(p. ex.: Crédito ou Débito etc.)" and nome_arq in ["MyPlan.csv","Myplan.csv","MYPLAN.csv","myplan.csv","myPlan.csv"]:
            pagamento_myplan = True
            uso_myplan = True
            if os.path.isfile(dire + "/Planilhas-MyCSV(Excel)/Tipo_de_pagamento-MyPlan.txt"):
                with open(dire + "/Planilhas-MyCSV(Excel)/Tipo_de_pagamento-MyPlan.txt","r") as text_r:
                    print('\nOs tipos de pagamento já utilizados na planilha foram:\n' + text_r.read())
                       
        info = input("-> {}: ".format(titulo)).strip()
        lst_infosordered += [info]
        if cate_myplan: text_categoria(info, dire);   cate_myplan = False
        elif pagamento_myplan: text_pagamento(info, dire);   pagamento_myplan = False
    
    if uso_myplan:
        lst_infosordered = analise_infos(lst_infosordered)
    else:
        lst_infosordered = [lst_infosordered]
    
    parada = False
    while parada == False:
        escolha4 = input('\nSE TODOS DADOS ESTIVEREM CORRETOS, APERTE ENTER PARA CONTINUAR.\nCaso contrário, DIGITE "n" ou qualquer outra LETRA para corrigí-los: ').strip()
        if escolha4 == "": adc_in_excel(lst_infosordered,path)
    
        if escolha4 != "":
            lst_infosordered = adc_infos(cabecalho,path,nome_arq,dire,cate_myplan,uso_myplan,pagamento_myplan,escolha4)
            
        else:   
            print(BARRA_SEPARADORA2+'\n')
            escolha2 = input("Deseja adicionar mais?(S/N): ").strip()
            if escolha2 != "" and escolha2 in "SimsimSIM":
                lst_infosordered = adc_infos(cabecalho,path,nome_arq,dire,cate_myplan,uso_myplan,pagamento_myplan)
            else:
                print()
                parada = True

#---
#1: ler 1ª coluna, referente ao que se trata cada coluna (usado para o passo #0.1)

def read_columns(path):
    '''(string) -> list
    RECEBE string referente ao nome do arquivo que contém a planilha no formato CSV
    RETORNA lista com o título de cada coluna como elementos
    '''
    #para ler apenas uma linha, usei essa fonte de pesquisa:<https://stackoverflow.com/questions/27264818/dont-understand-pythons-csv-reader-object>
    with open(path,'r') as planilha:
        leitura = csv.reader(planilha,delimiter=';')
        #Fonte: <https://www.w3schools.com/python/ref_func_next.asp> para entender a sintaxe da function next()
        #       caso a planilha já exista, porém está sem cabeçalho, a função read_columns retorna [] como default.
        return next(leitura, [])
       
#---
#3: função que pegará as informações e implementará-las no arquivo EXCEL     

def adc_in_excel(lst_infosordered,path):
    '''(list,string) -> NoneType
    RECEBE lista referente às novas informações a implementar e nome do arquivo para modificar
    RETORNA None
    '''
    #Fonte: <https://medium.com/@renatojlelis/opera%C3%A7%C3%B5es-em-arquivos-csv-com-python-1aee99273fd5>
    #       <https://www.it-swarm.dev/pt/python/acrescentar-nova-linha-ao-antigo-arquivo-csv-python/968000475/> #utilizado, pois "a" trocado por "w" faz com que o arquivo seja modificado
    with open(path,'a',newline='') as planilha:
        adc_line = csv.writer(planilha , delimiter = ";") #delimitador identificado no Excel
        adc_line.writerows(lst_infosordered)

#---
#4: função que repete os passos de adicionar novas informações

def adc_infos(cabecalho,path,nome_arq,dire,cate_myplan,uso_myplan,pagamento_myplan,escolha4=""):
    '''(list,string,string,string,bool,bool,bool,string) -> NoneType
    RECEBE lista com títulos do cabeçalho e nome do arquivo que contém a planilha para atualizá-la. Além disso, recebe o nome do arquivo e o diretório do disco logal do usuário
    RECEBE três booleanos referentes às condições acessadas se estiver usando a planilha MyPlan. RECEBE string para saber se o indivíduo está corrigindo ou adicionando novos dados.
    RETORNA None
    '''
    print()
    if escolha4 == "":
        print(BARRA_SEPARADORA2)
        print('Digite todas novas informações a seguir\nAPERTE ENTER CASO NÃO TENHA A INFORMAÇÃO DE DETERMINADA COLUNA\nUSE "." no lugar da "," ou no lugar de ";"!\n')
    lst_infosordered = [] #lista com todas informções que serão adicionadas na ordem
    for titulo in cabecalho:
        if uso_myplan and titulo == "Categoria da compra/pagamento(p. ex.: Alimento ou Conta de luz etc.)":
            cate_myplan = True
            if os.path.isfile(dire + "/Planilhas-MyCSV(Excel)/Categorias-MyPlan.txt"):
                with open(dire + "/Planilhas-MyCSV(Excel)/Categorias-MyPlan.txt","r") as text_r:
                    print('\nAs Categorias já utilizadas na planilha foram:\n' + text_r.read())
                    
        elif uso_myplan and titulo == "Tipo de pagamento(p. ex.: Crédito ou Débito etc.)":
            pagamento_myplan = True
            if os.path.isfile(dire + "/Planilhas-MyCSV(Excel)/Tipo_de_pagamento-MyPlan.txt"):
                with open(dire + "/Planilhas-MyCSV(Excel)/Tipo_de_pagamento-MyPlan.txt","r") as text_r:
                    print('\nOs tipos de pagamento já utilizados na planilha foram:\n' + text_r.read())
    
        info = input("-> {}: ".format(titulo)).strip()
        lst_infosordered += [info]
        if cate_myplan: text_categoria(info, dire);   cate_myplan = False
        elif pagamento_myplan: text_pagamento(info, dire);   pagamento_myplan = False
        
    if uso_myplan:
        lst_infosordered = analise_infos(lst_infosordered)
    else:
        lst_infosordered = [lst_infosordered]
        
    return lst_infosordered
    
#---
#5: função executável apenas se a condição do passo #0.1 for verdadeira, ou seja, apenas se a planilha já existir e o indivíduo desejar adicionar novos títulos ao cabeçalho (novas colunas)
def atualize_cab(adc,path):
    '''(string,string) -> NoneType
    RECEBE string referente ao(s) novo(s) título(s) de cabeçalho adiciono(s) e outra string referente ao nome do arquivo 
    RETORNA None
    '''    
    with open(path,'r') as arq_r:
        leitura = csv.reader(arq_r , delimiter=',') #a partir deste delimitador, a função identifica a separação dos valores em cada célula do arquivo CSV
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
        escrita = csv.writer(arq_w , delimiter=';')
        for linha in a[:-1]: #como '\n' foi usado para separar as linha em "new_doc", portanto foi preciso colocar esse intervalo ([:-1]) para não considerar o último elemento da lista "a" que é uma string vazia
            linha = linha.split(';')
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
#7.1: Função especial para a planilha "MyPlan". Identifica todas categorias de compra/pagemento registradas até então.
def text_categoria(info, dire):
    '''(string, string) -> NoneType
    RECEBE string para colocar no texto das Categorias de compra já citadas na planilha, caso o indivíduo estiver acessando a planilha "MyPlan" e outra string para localizar o arquivo de texto
    RETORNA None
    '''
    if info != "":
        with open(dire + "/Planilhas-MyCSV(Excel)/Categorias-MyPlan.txt", "a") as text_w, open(dire + "/Planilhas-MyCSV(Excel)/Categorias-MyPlan.txt", "r") as text_r:
            if info not in text_r.read():   text_w.write(' |' + info)

#---
#7.2: Função exclusiva para a planilha "MyPlan". Identifica todas tipos de pagemento registrados até então.
def text_pagamento(info, dire):
    '''(string, string) -> NoneType
    RECEBE string para colocar no texto dos Tipo de pagamento já citados na planilha, caso o indivíduo estiver acessando a planilha "MyPlan" e outra string para localizar o arquivo de texto
    RETORNA None
    '''
    if info != "":
        with open(dire + "/Planilhas-MyCSV(Excel)/Tipo_de_pagamento-MyPlan.txt", "a") as text_w, open(dire + "/Planilhas-MyCSV(Excel)/Tipo_de_pagamento-MyPlan.txt", "r") as text_r:
            if info not in text_r.read():   text_w.write(' |' + info)

#---
#8: Função mutável para preencher informações
def analise_infos(lst_infosordered):
    '''(list) -> list
    RECEBE lista referente às novas informações adicionadas
    RETORNA a lista com as informações a serem adicionadas na planilha
    '''
    lst_clone = lst_infosordered[:] #clone para conservar a lista orginal
    lst = [] #lista para ser preenchida com as informações tratadas
    
    #Em MyPlan.csv: [0]:Data; [1]:Ganhei; [2]:Paguei/Gastei; [3]:Parcelas; [4]:Troco/Sobrou; [5]:Trabalho feito; [6]:Compra feita; [7]:Categoria ;[8]Tipo de pagamento
    #Essas são as 8 principais colunas.
    #Saldo aparecerá no relatório do dashboard.
    
    #Tratar os dados:
    data_ini = lst_clone[0]
    
    if lst_clone[1] == "": ganho = 0
    else: ganho = round(abs(float(lst_infosordered[1])),2) #Arredondando para duas casas decimais. Assim o excel não considera o ponto como um milhar por exemplo. Fonte: <https://pt.stackoverflow.com/questions/176243/como-limitar-n%C3%BAmeros-decimais-em-python>
    
    if lst_clone[3] == "": parcelas = 1
    elif abs(int(lst_clone[3])) == 0: parcelas = 0
    elif abs(int(lst_clone[3])) > 1: parcelas = abs(int(lst_clone[3]))
    
    dia, mes, ano = formata_data(data_ini)
    troco = 0
    if parcelas > 1:
        gasto = round(abs(float(lst_clone[2]))/parcelas,2)
        datas_parcelas = lst_datas(dia,mes,ano,parcelas)
        lst_ref = [datas_parcelas[0],ganho,gasto,"1 de "+str(parcelas)+" parcelas",troco]
        for i in range(5,len(lst_clone)):
            lst_ref += [lst_clone[i]]
        lst += [lst_ref]
        j=2 # número da parcela, começando pela 2ª, visto que a 1ª já está adicionada na lista "lst"
        for date in datas_parcelas[1:]:
            lst += [[date,0,gasto,str(j)+" de "+str(parcelas)+" parcelas",0,""]+lst_clone[6:]]
            j+=1
        
        return lst
        
    else: 
        if lst_clone[4] != "": #Paguei e recebi determinado troco
            gasto = round(abs(float(lst_clone[2])) - abs(float(lst_clone[4])),2)
        else:
            if lst_clone[2] == "": gasto = 0
            else: gasto = round(abs(float(lst_clone[2])),2)
        lst_principal = [dia+'/'+mes+'/'+ano,ganho,gasto,parcelas,troco]
        for i in range(5,len(lst_clone)):
            lst_principal += [lst_clone[i]]
        lst = [lst_principal]
        
        return lst
    
#---
#9.0:
def formata_data(data_ini):
    '''(string) -> str, str, str
    RECEBE string referente à data inicial sem formatação
    RETORNA dia, mês e ano formatados
    '''
    num=''
    cont=1
    for char in data_ini:
        num += char
        if char == "/":
            if cont == 1:
                dia = num[:-1]
                cont += 1
                num = ''
            elif cont == 2:
                mes = num[:-1]
                cont += 1
                num = ''
    if len(num) == 1: ano = '200'+num #Até primeira década do milênio ¯\_(ツ)_/¯
    elif len(num) == 2: ano ='20'+num #mais comum de ter. Escrevendo só os últimos dois números do ano
    elif len(num) == 3: ano = '2'+num #atendendo à troca de século ( ͡• ͜ʖ ͡• )
    else: ano = num
    
    return dia, mes, ano

#---
#9.1:
def lst_datas(dia,mes,ano,parcelas):
    '''(string,int) -> list    
    RECEBE string da data inicial do pagamento das parcelas e número de parcelas
    RETORNA lista com as datas dos pagamentos das parcelas(mensais)    
    '''
    lst_datas = []

    #maxdias_meses_bissexto = [31,29,31,30,31,30,31,31,30,31,30,31]
    #maxdias_meses = [31,28,31,30,31,30,31,31,30,31,30,31]
    
    ano_a_mais = 0
    if int(dia) > 28:
        if int(dia) <= 30:
            for i in range(parcelas):
                mes_adc_total = int(mes)+i
                if mes_adc_total > 12:
                    if mes_adc_total%12 != 0: mes_adc = mes_adc_total%12
                    else: mes_adc = 12
                else: mes_adc = mes_adc_total
                if mes_adc == 2 and (int(ano)+ano_a_mais)%4 == 0: dia_adc = 29
                elif mes_adc == 2: dia_adc = 28
                else: dia_adc = int(dia)
                lst_datas += [str(dia_adc)+'/'+str(mes_adc)+'/'+str(int(ano)+ano_a_mais)]
                ano_a_mais = mes_adc_total//12
        else:
            for i in range(parcelas):
                mes_adc_total = int(mes)+i
                if mes_adc_total > 12:
                    if mes_adc_total%12 != 0: mes_adc = mes_adc_total%12
                    else: mes_adc = 12
                else: mes_adc = mes_adc_total
                if mes_adc == 2 and (int(ano)+ano_a_mais)%4 == 0: dia_adc = 29
                elif mes_adc == 2: dia_adc = 28
                else: 
                    if mes_adc in [4,6,9,11]: dia_adc = 30
                    else: dia_adc = 31
                
                lst_datas += [str(dia_adc)+'/'+str(mes_adc)+'/'+str(int(ano)+ano_a_mais)]
                ano_a_mais = mes_adc_total//12
                
    else:
        dia_adc = int(dia)
        for i in range(parcelas):
            mes_adc_total = int(mes)+i
            if mes_adc_total > 12:
                if mes_adc_total%12 != 0: mes_adc = mes_adc_total%12
                else: mes_adc = 12
            else: mes_adc = mes_adc_total
            
            lst_datas += [str(dia_adc)+'/'+str(mes_adc)+'/'+str(int(ano)+ano_a_mais)]
            ano_a_mais = mes_adc_total//12
    
    return lst_datas

#---
if __name__ == "__main__":
    main()







