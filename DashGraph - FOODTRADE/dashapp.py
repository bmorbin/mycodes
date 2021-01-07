# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 04:29:01 2020

@author: Bruno
"""
import json
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_cytoscape as cyto

app = dash.Dash(__name__,suppress_callback_exceptions = True)
app.tittle = "FOODTRADE IN SOUTH AMERICA COUNTRIES"
server=app.server

app.scripts.config.serve_locally = True
app.css.config.serve_locally     = True

# Loading Data of Importation
with open('importation_values.json','r') as f:
    data_imp = json.loads(f.read())

# Loading Data of Exportation
with open('exportation_values.json','r') as f:
    data_exp = json.loads(f.read())

# Preparing Data
def reset_data(data):
    nodes = [n for n in data if "id" in n["data"].keys()]
    edges = [n for n in data if "source" in n["data"].keys()]
    return nodes, edges

nodes_exp, edges_exp = reset_data(data_exp)
nodes_imp, edges_imp = reset_data(data_imp)

# Obs.: como tanto em data_imp como em data_exp tem-se os mesmos países, não
#       importa qual data escolher neste caso.
countries = [n for n in data_imp if "id" in n["data"].keys() and n["classes"]=='pais']
countries = {n["data"]["id"] for n in countries}
countries_opt = []
for name in sorted(countries):
    countries_opt.append({"label": name,
                          "value": name})

#Solucionador do problema com enconding: https://humberto.io/pt-br/blog/tldr-leitura-e-escrita-de-unicode-em-arquivos-com-python-2-e-3/
#Adaptações: usei o decode(latin-1) pq o utf-8 não funcionou E colocar 'rb' ao inves de 'r' E colocar '\r' no split
#Sem seguir esses passos, dava problema com o nome "Maté" por exemplo, por conta da acentuação
with open('produto_imp_elements.txt','rb') as file:
    produto_imp_elements = file.read().decode('latin-1').split('\r\n')
produto_imp_elements.pop()
produtos_imp_opt=[]
for name in produto_imp_elements:
    produtos_imp_opt.append({'label':name,
                            'value':name})

with open('produto_exp_elements.txt','rb') as file:
    produto_exp_elements = file.read().decode('latin-1').split('\r\n')
produto_exp_elements.pop()
produtos_exp_opt=[]

for name in produto_exp_elements:
    produtos_exp_opt.append({'label':name,
                        'value':name})

#Nota: percebeu-se que as listas de animais exportados e de, importados são iguais
with open('animal_exp_elements.txt','rb') as file:
    animals_elements = file.read().decode('latin-1').split('\r\n')
animals_elements.pop()
animals_opt=[]
for name in animals_elements:
    animals_opt.append({'label':name,
                        'value':name})

#=============================================================================
# Complementary selections
def select_nodes_by_edges(nodes, edges):
    set1 = set([e["data"]["source"] for e in edges])
    set2 = set([e["data"]["target"] for e in edges])
    e = set1.union(set2)
    selected = [n for n in nodes if (n["data"]["name"] in e)]
    return selected

def select_edges_by_nodes(nodes, edges):
    esps = [d["data"]["name"] for d in nodes]
    selected = [e for e in edges if (e["data"]["source"] in esps) and (e["data"]["target"] in esps)]
    return selected

#=============================================================================
# For selecting by countries
def select_by_countries(nodes,edges,countries):
    '''(list,list,list) -> list,list
    RECEBE  listas dos nós, das arestas, e do país(es) selecionado(s).
    RETORNA lista dos nós que são vizinhos dos países selecionados e seus
            sucessores e as respectivas arestas.
    '''

    sel_edges = [e for e in edges if (e["data"]["source"] in countries) or (e["data"]["target"] in countries)]
    sel_nodes = select_nodes_by_edges(nodes,sel_edges)
    sel_edges = select_edges_by_nodes(sel_nodes,edges)
    return sel_nodes, sel_edges

#=============================================================================
# For selecting by years
def select_by_years(nodes,edges,years):
    '''(list,list,list) -> list,list
    RECEBE  listas dos nós, das arestas, e do ano(s) selecionado(s).
    RETORNA lista dos nós que são vizinhos dos países selecionados e seus
            sucessores e as respectivas arestas.
    '''
    sel_edges= [e for e in edges if(boolean_sel_edges_years(e,years))]
    sel_nodes = select_nodes_by_edges(nodes,sel_edges)
    # sel_edges = select_edges_by_nodes(sel_nodes,edges)
    return sel_nodes, sel_edges

def boolean_sel_edges_years(e,years):
    busca=''
    for ano in years:
        busca+=str(ano)
    if e['data'][busca] != 'US$0.00':
        return True
    return False

#=============================================================================
# For selecting by elements
def select_by_elements(nodes,edges,elements):
    '''(list,list,list) -> list,list
    RECEBE  listas dos nós, das arestas, e do elemento(s) selecionado(s).
    RETORNA lista dos nós que são vizinhos dos países selecionados e
            seus sucessores e as respectivas arestas.
    '''
    i=0
    f=len(elements)
    parada=False
    all_animals=False
    all_crops=False

    while i<f and not parada:
        if elements[i] == 'null-animals':
            all_animals=True
        elif elements[i] == 'null-crops':
            all_crops=True
        if all_animals and all_crops:
            parada=True
        i+=1

    if all_crops and all_animals:
        return nodes,edges
    elif all_crops:
        sel_nodes_animals = [n for n in nodes if (n['data']['name'] in elements and n['classes']=='animal')]
        sel_nodes_crops = [n for n in nodes if(n['classes']=='produto' or n['classes'] == 'pais')]
        sel_nodes = sel_nodes_animals + sel_nodes_crops
    elif all_animals:
        sel_nodes_crops = [n for n in nodes if(n['data']['name'] in elements and n['classes']=='produto')]
        sel_nodes_animals = [n for n in nodes if (n['classes']=='animal' or n['classes'] == 'pais')]
        sel_nodes = sel_nodes_animals + sel_nodes_crops
    else:
        sel_nodes = [n for n in nodes if (n['data']['name'] in elements) or (n['classes'] == 'pais')]

    sel_edges = select_edges_by_nodes(sel_nodes, edges)
    return sel_nodes, sel_edges

#=============================================================================
# Loading Stylesheet
with open('my-style.json','r') as f:
    stylesheet = json.loads(f.read())


styles = {'cytoscape':{'width':'80%',
                       'height':'100%',
                       'background-transparent':True,
                      },
          "container":{'position': 'fixed',
                       'top':'0px',
                       'bottom':'0px',
                       'right':'0px',
                       'left':'0px',
                       'height': '100%',
                       'width': '100%',
                       'font-family':'Sans Serif, sans-serif',
                       'line-height': 'normal',
                       'color':'white',
                       # 'justify-content':'center',
                       # 'background-color':'#0a0a0a',
                       'background-image':"url('https://i.postimg.cc/TP1HBqqF/bg-html-Prancheta-1.png')",
                       'background-repeat': 'no-repeat',
                       'background-attachment': 'fixed',
                       'background-size':'100% 100%'
                      },
          "Table":{'position':'fixed',
                   'background-color':'rgb(0,0,0,0.8)',
                   'height': '100%',
                   'width': '20%',
                   'top':'0px',
                   'bottom':'0px',
                   'right':'0px',
                   'left':'80%',
                   'font-family':'sans-serif',
                   'font-size':'13px',
                   # 'line-height': '0px',
                   'color':'white',
                   'textAlign':'center',
                   'overflowY':'visible',
                   'overflowX':'hidden'
                  },
          'Tab_style_imp':{'borderTop': '6px solid #4d0000',
                           'borderLeft':'none',
                           'borderRight':'none',
                           'borderBottom':'none',
                           'color':'white',
                           'background-color':'#0D0D0D',
                           'font-size':'12px',
                           'width':"50%"
                          },
          'Tab_selected_imp':{'borderTop': '6px solid #ff0000',
                              'borderLeft':'none',
                              'borderRight':'none',
                              'color':'white',
                              'background-color':'rgb(0,0,0,0)',
                              'fontWeight':'bold',
                              'font-size':'14px',
                              'width':"50%"
                             },
          'Tab_style_exp':{'borderTop': '6px solid #002402',
                           'borderLeft':'none',
                           'borderRight':'none',
                           'borderBottom':'none',
                           'color':'white',
                           'background-color':'#0D0D0D',
                           'font-size':'12px',
                           'width':"50%"
                           },
          'Tab_selected_exp':{'borderTop': '6px solid #1bff00',
                              'borderLeft':'none',
                              'borderRight':'none',
                              'color':'white',
                              'background-color':'rgb(0,0,0,0)',
                              'fontWeight':'bold',
                              'font-size':'14px',
                              'width':"50%"
                              },
          'Subtitle':{'position': 'absolute',
                      'display':'block',
                      'top':'10px',
                      'left':'10px',
                      # 'height': '3.5%',
                      # 'width': '15%',
                      'textAlign':'left',
                      # 'marginTop':'1%',
                      # 'marginLeft':'1%',
                      'color':'white',
                      'font-family':'sans-serif',
                      'font-size':'14px',
                      'cursor': 'pointer',
                      'marginBottom':'10px'
                      },
          'Subtitle-content':{'position':'relative',
                              #'position': 'fixed',
                              'display':'block',
                              # 'top':'20px',
                              # 'bottom':'0%',
                              # 'right':'0%',
                              # 'left':'0.8%',
                              # 'height': '83.531408px',
                              'width': '15%',
                              'font-family':'Segoe UI,sans-serif',
                              'font-size':'13px',
                              'color':'white',
                              'textAlign':'center',
                              'marginTop':'30px',
                              # 'background-image':"url('https://i.postimg.cc/nhkLRJT0/subtitle.png')",
                              # 'background-repeat': 'no-repeat',
                              # 'background-size':'100% 100%',
                              'background-color':'rgb(0,0,0,0.8)',
                              'border':'1px solid rgb(0,0,0)',
                              'border-radius':'5px'
                              },
          'Complements':{'position': 'relative',
                         'display':'block',
                         'top':'0%',
                         'bottom':'0px',
                         'right':'0px',
                         'left':'0%',
                         'textAlign':'left',
                         'color':'white',
                         'marginTop':'0px',
                         'marginLeft':'1px',
                         'font-family':'sans-serif',
                         'font-size':'11px',}
         }

Tb_Imp = [html.Br(),
          html.Button(id='reset-buttom-imp',
                      children=['RESET'],
                      style={'background-color':'#c90043',
                             'border':'3px solid #c90043',
                             'color':'white',
                             'fontWeight':'Bold',
                             'border-radius':'5px',
                              'marginBottom':'4px',
                              'font-size':'13px',
                              'cursor': 'pointer'
                             }),
          html.Br(),
          html.Label('OR',style={'fontWeight':'Bold',}),
          html.Br(),
          html.Label('Choose for specific...'),
          html.Details([
          html.Summary(children=['Time interval'],style={'background-color':'#c90043','textAlign':'left','textIndent':'10px','marginTop':'10px','cursor': 'pointer'}),
          html.Br(),
          dcc.RangeSlider(id='imp-years-slider',
                          marks={i:"{}".format(i) for i in range(2014, 2019)},
                          min=2014,
                          max=2018,
                          value=[2014,2018],
                          step=None,
                          allowCross=False,
                          )]),
          # html.Br(),
          html.Details([
          html.Summary(children=['Countries'],style={'background-color':'#c90043','textAlign':'left','textIndent':'10px','marginTop':'10px','cursor': 'pointer'}),
          html.Div([dcc.Checklist(id='imp-countries-checklist',
                                  options = [{"label":'All countries','value':"null"}] + countries_opt,
                                  value = ['null'],
                                  labelStyle={'position':'relative',
                                              'height':'100%',
                                              'display': 'block',
                                              'textAlign':'left',
                                              'line-height':'normal',
                                              'fontWeight':'100',
                                              'font-size':'12px',
                                              'verticalAlign':'middle'
                                              },
                                  inputClassName='btn'
                        )])]),
          html.Details([
          html.Summary(children=['Live animals'],style={'background-color':'#c90043','textAlign':'left','textIndent':'10px','marginTop':'10px','cursor': 'pointer'}),
          html.Div([dcc.Dropdown(id='imp-liveanimals-dropdown',
                                 multi=True,
                                 options=[{'label':'All live animals','value':'null-animals'}]+animals_opt,
                                 value=['null-animals'],
                                 style={'width': '100%',
                                        'height':'100%',
                                        'display':'block',
                                        'color':'black',
                                        'marginBottom':'0px'
                                        },
                                 placeholder='Select or Type it...',
                                 disabled=False
                                 )],className='custom-dropdown'
                    ),
          html.Div(dcc.Markdown("Source: [(FAOSTAT: Live animals Trade)] (http://www.fao.org/faostat/en/#data/TA). Accessed on Sep 18, 2020."),style=styles['Complements'])]),
          html.Details([
          html.Summary(children=['Crops and livestock products'],style={'background-color':'#c90043','textAlign':'left','textIndent':'10px','marginTop':'10px','cursor': 'pointer'}),
          html.Div([dcc.Dropdown(id='imp-products-dropdown',
                                 multi=True,
                                 options=[{'label':'All crops and livestock products','value':'null-crops'}]+produtos_imp_opt,
                                 value=['null-crops'],
                                 style={'width': '100%',
                                        'height':'100%',
                                        'display':'block',
                                        'color':'black',
                                        'marginBottom':'0px'
                                        },
                                 placeholder='Select or Type it...',
                                 disabled=False
                                 )],className='custom-dropdown'
                    ),
          html.Div(dcc.Markdown("Source: [(FAOSTAT: Crops and livestock products Trade)] (http://www.fao.org/faostat/en/#data/TP). Accessed on Sep 18, 2020."),style=styles['Complements'])]),
          ]

Tb_Exp = [html.Br(),
          html.Button(id='reset-buttom-exp',
                      children=['RESET'],
                      style={'background-color':'#c90043',
                             'border':'3px solid #c90043',
                             'color':'white',
                             'fontWeight':'Bold',
                             'border-radius':'5px',
                              'marginBottom':'4px',
                              'font-size':'13px',
                              'cursor': 'pointer'
                             }),
          html.Br(),
          html.Label('OR',style={'fontWeight':'Bold',}),
          html.Br(),
          html.Label('Choose for specific...'),
          html.Details([
          html.Summary(children=['Time interval'],style={'background-color':'#c90043','textAlign':'left','textIndent':'10px','marginTop':'10px','cursor': 'pointer'}),
          html.Br(),
          dcc.RangeSlider(id='exp-years-slider',
                          marks={i:"{}".format(i) for i in range(2014, 2019)},
                          min=2014,
                          max=2018,
                          value=[2014,2018],
                          step=None,
                          allowCross=False,
                          )]),
          # html.Br(),
          html.Details([
          html.Summary(children=['Countries'],style={'background-color':'#c90043','textAlign':'left','textIndent':'10px','marginTop':'10px','cursor': 'pointer'}),
          html.Div([dcc.Checklist(id='exp-countries-checklist',
                                  options = [{"label":'All countries','value':"null"}] + countries_opt,
                                  value = ['null'],
                                  labelStyle={'position':'relative',
                                              'height':'100%',
                                              'display': 'block',
                                              'textAlign':'left',
                                              'line-height':'normal',
                                              'fontWeight':'100',
                                              'font-size':'12px',
                                              'verticalAlign':'middle'
                                              },
                                  inputClassName='btn'
                        )])]),
          html.Details([
          html.Summary(children=['Live animals'],style={'background-color':'#c90043','textAlign':'left','textIndent':'10px','marginTop':'10px','cursor': 'pointer'}),
          html.Div([dcc.Dropdown(id='exp-liveanimals-dropdown',
                                 multi=True,
                                 options=[{'label':'All live animals','value':'null-animals'}]+animals_opt,
                                 value=['null-animals'],
                                 style={'width': '100%',
                                        'height':'100%',
                                        'display':'block',
                                        'color':'black',
                                        'marginBottom':'0px'
                                        },
                                 placeholder='Select or Type it...',
                                 disabled=False
                                 )],className='custom-dropdown'
                    ),
          html.Div(dcc.Markdown("Source: [(FAOSTAT: Live animals Trade)] (http://www.fao.org/faostat/en/#data/TA). Accessed on Sep 18, 2020."),style=styles['Complements'])]),
          html.Details([
          html.Summary(children=['Crops and livestock products'],style={'background-color':'#c90043','textAlign':'left','textIndent':'10px','marginTop':'10px','cursor': 'pointer'}),
          html.Div([dcc.Dropdown(id='exp-products-dropdown',
                                 multi=True,
                                 options=[{'label':'All crops and livestock products','value':'null-crops'}]+produtos_exp_opt,
                                 value=['null-crops'],
                                 style={'width': '100%',
                                        'height':'100%',
                                        'display':'block',
                                        'color':'black',
                                        'marginBottom':'0px'
                                        },
                                 placeholder='Select or Type it...',
                                 disabled=False
                                 )],className='custom-dropdown'
                    ),
          html.Div(children=[dcc.Markdown("Source: [(FAOSTAT: Crops and livestock products Trade)] (http://www.fao.org/faostat/en/#data/TP). Accessed on Sep 18, 2020.")],style=styles['Complements'])]),
          ]



app.layout = html.Div([html.Div(style=styles['container'],
                       children=[cyto.Cytoscape(id='cytoscape-graph',
                                                elements = nodes_imp+edges_imp,
                                                stylesheet=stylesheet,
                                                style= styles['cytoscape'],
                                                layout={'name':'concentric', #https://github.com/cytoscape/cytoscape.js/blob/master/documentation/demos/concentric-layout/code.js
                                                        'minDistance':0,
                                                        'maxDistance':0,
                                                        'padding': 0,
                                                        'equidistant':False,
                                                        'minNodeSpacing': 0,
                                                        'height': 0,
                                                        'width':0,
                                                        'avoidOverlap':False,
                                                        'spacingFactor':5,
                                                        'fit':True,
                                                        'refresh':False,
                                                        },
                                                responsive=True
                                               )
                                 ]
                                ),
                       # html.Div(style=styles['Subtitle']),
                       html.Details([
                       html.Summary(children=['Subtitle'],style=styles['Subtitle']),
                       html.Div(children=[html.Label(children=['PINK TRIANGLE'],style={'color':'#d90082','fontWeight':'bolder','text-decoration': 'underline'}), html.Label(children=['  represents']),html.Br(),html.Label(children=['Live animals'],style={"color": "gold"}),html.Br(),html.Label('—'),html.Br(),html.Label(children=['GREEN CIRCLE'],style={'text-decoration': 'underline','color':'#24592f','fontWeight':'bolder'}), html.Label(children=['  represents']),html.Br(), html.Label(children=['Crops and livestock products'],style={"color": "gold"})],style=styles['Subtitle-content'])]),
                       html.Div(children=['Created by Bruno Groper Morbin©'],style={'position': 'absolute',
                                                                                    'bottom':'10px',
                                                                                    'left':'10px',
                                                                                    'textAlign':'left',
                                                                                    'color':'white',
                                                                                    'font-family':'Segoe UI Light, sans-serif',
                                                                                    'font-size':'10px',
                                                                                    'opacity':'0.8'}),
                       html.Div(style=styles['Table'],
                                children = [dcc.Tabs(id='tabs-imp-exp',
                                                     children=[dcc.Tab(label='Importation',
                                                                       value='tab-imp',
                                                                       style=styles['Tab_style_imp'],
                                                                       selected_style=styles['Tab_selected_imp'],
                                                                       children=Tb_Imp),
                                                               dcc.Tab(label='Exportation',
                                                                       value='tab-exp',
                                                                       style=styles['Tab_style_exp'],
                                                                       selected_style=styles['Tab_selected_exp'],
                                                                       children=Tb_Exp)
                                                               ],
                                                     value='tab-imp',
                                                    )]
                                ),

                       ]
             )

@app.callback(Output(component_id = 'cytoscape-graph',component_property = 'elements'),
              Output(component_id = 'cytoscape-graph',component_property = 'stylesheet'),
              Input('imp-years-slider', 'value'),
              Input('imp-countries-checklist', 'value'),
              Input('imp-liveanimals-dropdown', 'value'),
              Input('imp-products-dropdown', 'value'),
              Input('exp-years-slider', 'value'),
              Input('exp-countries-checklist', 'value'),
              Input('exp-liveanimals-dropdown', 'value'),
              Input('exp-products-dropdown', 'value'),
              Input('tabs-imp-exp','value'))
def confirm_tab_imp(time_interval_imp,list_countries_imp,list_animals_imp,list_products_imp,time_interval_exp,list_countries_exp,list_animals_exp,list_products_exp,value_tab):
    if value_tab == 'tab-imp':
        return update_graph(time_interval_imp,list_countries_imp,list_animals_imp,list_products_imp,data_imp)
    else:
        return update_graph(time_interval_exp,list_countries_exp,list_animals_exp,list_products_exp,data_exp)

def update_graph(time_interval,list_countries,list_animals,list_products,data):
    nodes,edges= reset_data(data)

    if list_countries is not None and 'null' not in list_countries:
        nodes,edges = select_by_countries(nodes,edges,list_countries)

    list_elements = list_animals + list_products
    if list_elements is not None:
        nodes,edges = select_by_elements(nodes, edges, list_elements)

    list_years = [i for i in range(time_interval[0],time_interval[-1]+1)]
    if list_years is not None and list_years != []:
        nodes,edges = select_by_years(nodes,edges,list_years)

    years_code = ''
    for ano in list_years:
        years_code += str(ano)

    custom_stylesheet = stylesheet + [{"selector":"edge","style":{"label": "data({})".format(years_code)}}]

    return nodes+edges, custom_stylesheet

@app.callback(Output('imp-years-slider', 'value'),
              Output('imp-countries-checklist', 'value'),
              Output('imp-liveanimals-dropdown', 'value'),
              Output('imp-products-dropdown', 'value'),
              Input('reset-buttom-imp','n_clicks'))
def reset_imp(click):
    return [2014,2018],['null'],['null-animals'],['null-crops']

@app.callback(Output('exp-years-slider', 'value'),
              Output('exp-countries-checklist', 'value'),
              Output('exp-liveanimals-dropdown', 'value'),
              Output('exp-products-dropdown', 'value'),
              Input('reset-buttom-exp','n_clicks'))
def reset_exp(click):
    return [2014,2018],['null'],['null-animals'],['null-crops']

if __name__ == '__main__':
    app.run_server(debug=True)

