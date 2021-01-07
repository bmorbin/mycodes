# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 23:46:31 2020

@author: Bruno
"""
def command_show(entrada):
    cur.execute(entrada)
    show_input_mysql(entrada)
    show_output_mysql()

def show_input_mysql(entrada):
    print("mysql> ",end="")
    print(entrada,end=";\n")

def show_output_mysql():
    for r in cur.fetchall():
        print('\t'+str(r))

# ============================================================================
# Acessing MySQL
import getpass
import pymysql

# p = getpass.getpass()
p = input("Coloque sua senha: ")
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd = p)
cur = conn.cursor()

entrada="SHOW DATABASES"
command_show(entrada)

DB=input("Digite o nome do DB a ser usado:\t")
entrada=f"USE {DB}"
command_show(entrada)

entrada="SHOW TABLES"
command_show(entrada)

def describe_table():
    table=input("Digite o nome da tabela a ser descrita (OU APERTE ENTER PARA PASSAR):\n\t")
    while table!="":
        command_show(f"DESCRIBE {table}")
        table=input("Digite o nome da tabela a ser descrita (OU APERTE ENTER PARA PASSAR):\n\t")

# ============================================================================
# Selecting personalized table & Transform to dataframe 
# Using SQLAlchemy and Pandas
from sqlalchemy import create_engine
import pandas as pd
from urllib.parse import quote_plus as urlquote #Fonte: https://stackoverflow.com/questions/15728290/sqlalchemy-valueerror-for-slash-in-password-for-create-engine

# Conecting SQLAlchemy to MySQL 
engineString = f'mysql://root:%s@localhost/{DB}' % urlquote(p)
engine = create_engine(engineString)

# ============================================================================
# Using dataframe generated from above to generate a Graph with NetworkX
import networkx as nx
import json
import math
s=set()

def main():
    grafo()
    stylesheet = [
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)',
            # 'shape':'rectangle',
            "width": "60%",
            "height": "60%",
            "font-size": "30px",
            "text-valign": "center",
            "text-halign": "center",
            "text-outline-color": "#000",
            "text-outline-width": "5px",
            "color": "#F4CE00",
            "overlay-padding": "6px"
        }
    },
    {
        'selector': '.pais',
        'style': {
            'background-fit': 'cover',
            'background-image': 'data(url)',
            'width': "150%",
            'height': "100%",
            'shape':'rectangle',
            "text-valign": "bottom", #https://developer.mozilla.org/pt-BR/docs/Web/CSS/vertical-align
            "text-halign": "center"
        }
    },
    {
         'selector': 'edge',
         'style': {
              'line-color': 'data(color)',
              'font-size': '20px',
              "text-outline-color": "#000",
              "text-outline-width": "5px",
              "text-valign": "baseline",
              "text-halign": "baseline",
              'color':'white',
              'source-arrow-shape': 'triangle',
              'source-arrow-color': 'data(color)',
              'curve-style': 'bezier',
              "opacity": "1",
              "width": "0.5",
              "overlay-padding": "0.5px"
        }
     }
    ]
    
    for tipo in s:
        if 'animal' in tipo:
            stylesheet.append(
            {
                'selector': tipo,
                'style': {
                    'background-color': 'data(color)',
                    'shape':'triangle'
                    # 'width': "data(size)",
                    # 'height': "data(size)",
                }
            }
            )
        else:
            stylesheet.append(
            {
                'selector': tipo,
                'style': {
                    'background-color': 'data(color)',
                    'shape':'circle'
                    # 'width': "data(size)",
                    # 'height': "data(size)",
                }
            }
            )
    s.clear()
    
    mais_um = input("Deseja criar mais um grafo? [s/n]:\t")
    if mais_um != "" and mais_um in "sS":
        grafo()
        for tipo in s:
            if 'animal' in tipo:
                stylesheet.append(
                {
                    'selector': tipo,
                    'style': {
                        'background-color': 'data(color)',
                        'shape':'triangle'
                        # 'width': "data(size)",
                        # 'height': "data(size)",
                    }
                }
                )
            else:
                stylesheet.append(
                {
                    'selector': tipo,
                    'style': {
                        'background-color': 'data(color)',
                        'shape':'circle'
                        # 'width': "data(size)",
                        # 'height': "data(size)",
                    }
                }
                )
        s.clear()
        
    with open('my-style.json', 'w') as f:
        f.write(json.dumps(stylesheet))

def grafo():
    # Generando o grafo vazio
    G=nx.DiGraph()
    
    G = constroi_grafo(G)
    
    continua = input("APERTE ENTER PARA CONTINUAR\n")
    if continua == "":
        G = constroi_grafo(G)
    
    return G

def constroi_grafo(G):
    olhar_tabela = (input("Deseja olhar a descrição de alguma tabela? [s/n]: ")).strip()
    if olhar_tabela != "" and olhar_tabela in "sS":
        describe_table()
    
    QUERY=input('Digite o comando para gerar a tabela personalizada:\n')
    command_show(QUERY)
    # Exemplo de comando: SELECT nome_pais AS pais,anos_ano AS ano,animal,valor AS valor_Heads FROM animal_exp_quantity INNER JOIN paises ON paises_id_pais=id_pais WHERE anos_ano=2018
    
    #Fonte: https://pt.stackoverflow.com/questions/91012/transformar-query-em-dataframe-sqlalchemy-pandas
    df = pd.read_sql_query(QUERY, engine)
    df.info()
    df.head()
    
    colunas = (input("Digite o nome das colunas na ordem em que elas aparecem e as separando por ESPAÇO\n(Exemplo:PAIS ESPÉCIE ANO VALOR URL):\n\t")).split(" ")
    
    color_especie = input("Digite um código da cor desejável para os nós das espécies em questão:\
                          (Exemplos: #24592f -> verde musgo; #d90082 -> rosa)\n\t")
    
    color_edge = input("Digite um código da cor desejável para as arestas que conectarão pais e especie:\
                       (Exemplo:#00FF00 -> verde; #FF0000 -> vermelho)\n\t")
                           
    nodetype_especie = input("Classifique o tipo dos dados da coluna das espécies.\
                             Exemplo: animal OU produto\n\t")
                             
    edgetype = input("Nomeie as arestas que ligarão os países e as espécies:\
                     Exemplo: exportation OU importation\n\t")
                           
    for idx in df.index:
        especie = df.loc[idx,colunas[1]]
        pais = df.loc[idx,colunas[0]]
        ano = df.loc[idx, colunas[2]]
        valor = df.loc[idx, colunas[3]]
        
        # Adicionando nós com o nome das espécies e nós com o nome dos países
        if especie not in G:
            G.add_node(especie,
                       color=color_especie,
                       nodetype= nodetype_especie,
                       frequency = 1,
                       )
            s.add('.' + nodetype_especie)
        else:
            G.nodes[especie]['frequency'] += 1
        
        if pais not in G:
            G.add_node(pais,
                       color= df.loc[idx,colunas[4]], #URL da imagem da bandeira do pais
                       nodetype='pais',
                       frequency=1,
                       size=1
                       )
        else:
            G.nodes[pais]['frequency'] += 1
            G.nodes[pais]['size'] += 1
    
        # Adicionando arestas entre países e especies
        if not G.has_edge(pais, especie):
            G.add_edge(pais, 
                       especie, 
                       frequency = 1, 
                       color = color_edge,
                       edgetype = edgetype,
                       size=d.copy(),
                       )
            incrementa_valor(pais,especie,valor,ano,G)
        else:
            G.edges[pais, especie]['frequency'] += 1
            incrementa_valor(pais,especie,valor,ano,G)
    
    # Verificando atributos dados
    for node in G.nodes(data=True):
        print(node)
        break
    for edge in G.edges(data=True):
        print(edge)
        break
    
    resp = input("APERTE ENTER PARA SALVAR O GRAFO EM ARQUIVO JSON\
                 Caso contrário, digite qualquer coisa.\n")
    if resp == "":
        nome_arq = input("Nomeie o arquivo:\n\t")
        
        # Criação da estrutura JSON que será utilizada para criar grafo no Cytoscape:
        nodes = [{'data': {'id': node,
                           # 'value': d['size'],
                           'name': node,
                           'label': node,
                           'color': d['color'],
                           'url' :d['color']
                           },
                  'classes': d['nodetype']
                  }
                 for node, d in G.nodes(data=True)]
        
        edges = edges_json(G)
        
        elements = nodes + edges
        
        # Generating JSON file
        with open(nome_arq+'.json', 'w') as f:
            f.write(json.dumps(elements))

    return G

def edges_json(G):
    edges=[]
    for e1,e2,d in G.edges(data=True):
        info={'data': {'source': e1,
                       'target': e2,
                       'color': d['color'],
                       'frequency': d['frequency'],
                       'label': d['edgetype'],
                       },
              'classes':d['edgetype']}
        for c in d['size']:
            s=''
            for ano in c:
                s+=str(ano)
            info['data'][s] = 'US$' + str(d['size'][c]) + '.00'
        edges.append(info)    
    return edges

def incrementa_valor(pais,especie,valor,ano,G):
    for i in combs: 
        if ano in i:
            G.edges[pais, especie]['size'][i] += int(valor)
    
list_anos = [2014,2015,2016,2017,2018]
l=[]
for i in range(1,6):
    for j in range(0,5):
        adc = list_anos[j:j+i]
        l.append(adc)
d={}
for comb in l:
    d[tuple(comb)]=0

combs = d.keys()

main()
