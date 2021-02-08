import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import xml.etree.ElementTree as ET
import os

index_layout = html.Div(children=[
    html.H1(children='Class Services - Dashboard'),

    html.Div(children='''
        Faça login para poder entrar no dashboard
    '''),

    dcc.Link('Clique aqui', href='/login/', refresh=True)
])


def get_layout(session):
    file_name = ''
    tree = ET.parse(file_name)
    root = tree.getroot()

    names_1 = []
    names_2 = []
    path = list(root.find('users'))
    for user in path:
        names_1.append(user.attrib['username'])
        names_2.append(user.text)

    tab_names = go.Figure(data=[go.Table(header=dict(values=['Nomes de usuário', 'Nomes reais']),
                                         cells=dict(values=[names_1, names_2]))
                                ])

    user_name = []
    message_numbers = []
    path = list(root.find('ranking'))
    for user in path:
        user_name.append(user.attrib['username'])
        message_numbers.append(user.text)

    ranking = go.Figure(data=[go.Table(header=dict(values=['Nomes de usuário', 'Número de mensagens']),
                                       cells=dict(values=[user_name, message_numbers]))
                              ])

    pie_ranking = px.pie(pd.DataFrame({'Usuário': user_name, 'Mensagens': message_numbers}), values='Mensagens',
                         names='Usuário', title="Ranking - Gráfico de pizza")

    bots_count = root.find('usercount').attrib['bots']
    user_count = root.find('usercount').attrib['real_users']

    users_in_server_df = pd.DataFrame({'Tipo de usuário': ['Bot', 'Pessoa'], 'Contagem': [bots_count, user_count]})
    pie_count = px.pie(users_in_server_df, values='Contagem', names='Tipo de usuário', title="Contagem de usuários")

    dashboard_layout = html.Div(children=[
        html.H1(children='ClassServices - Dashboard'),

        dcc.Graph(
            id='tab_get_names',
            figure=tab_names
        ),

        dcc.Graph(
            id='tab_ranking',
            figure=ranking
        ),

        dcc.Graph(
            id='pizza_ranking',
            figure=pie_ranking
        ),

        dcc.Graph(
            id='pizza_count',
            figure=pie_count)
    ])

    return dashboard_layout
