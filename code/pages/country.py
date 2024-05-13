import pandas as pd
import dash
import plotly.graph_objects as go
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import time
import plotly.express as px


df = pd.read_csv("C:/Users/narig/OneDrive/Ambiente de Trabalho/VAD - Visualização Avançada de Dados/Projeto_final/VAD/datasets/dataset.csv")

dash.register_page(__name__, path='/country') 

navbar = html.Nav(
    
    className="navbar navbar-expand navbar-light bg-light",
    children=[
        html.A(className="navbar-anchor", href="#"),
        
        html.Span("Food", className="navbar-icon-Food"),
        html.Span("Waste", className="navbar-icon-Waste"),
        
        dcc.Link(
                f"{'Landing Page'}", href='/',className="navbar-body"
            ),
        dcc.Link(
                f"{'World'}", href='/world',className="navbar-body"
            ),
        dcc.Link(
                f"{'Country'}", href='/contry',className="navbar-body"
            ),
        dcc.Link(
                f"{'Product'}", href='/product',className="navbar-body"
            ),
    ]
)

layout = html.Div(id='contry_page',style={'background-color': 'rgb(240, 240, 240)', 'color': 'rgb(240, 240, 220)'}, children=[
    dcc.Location(id='contry_page', refresh=False),
    html.Div([
        html.Div([
                dcc.Dropdown(
                    id='order-selector_contry',
                    options=[
                        {'label': 'Crescent', 'value': 'crescente'},
                        {'label': 'Decrescent', 'value': 'decrescente'},
                    ],
                    value='crescente',
                    placeholder="Order",
                    style={'width': '25%', 'display': 'inline-block', 'background-color': 'green'}
                ),
                dcc.Dropdown(
                    id='size-selector_contry',
                    options=[
                        {'label': 'Top 10', 'value': 'top 10'},
                        {'label': 'Top 100', 'value': 'top 100'},
                        {'label': 'All', 'value': 'all'},
                    ],
                    value='top 10',
                    placeholder="Size",
                    style={'width': '25%', 'display': 'inline-block', 'background-color': 'green'}
                ),  
                dcc.Dropdown(
                    id='stats-selector_contry',
                    options=[
                        {'label': 'Média', 'value': 'media'},
                        {'label': 'Instâncias', 'value': 'instancias'},
                    ],
                    value='media',
                    placeholder="Stats",
                    style={'width': '25%', 'display': 'inline-block', 'background-color': 'green'}
                ),
                dcc.Dropdown(
                    id='contry_selector',
                    options=sorted([{'label': country, 'value': country} for country in df['country'].unique()], key=lambda x: x['label']),
                    value=df['country'].unique()[0],
                    placeholder="Country",
                    searchable=True,
                    style={'width': '25%', 'display': 'inline-block', 'background-color': 'green'}
                ), 
            ], style={'width': '100%', 'display': 'inline-block'}),

            html.Div(id='graph-container2', style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'})
    ]),         
])

def generate_graph_loss(df, country, is_mean):
    result = df[df['country'] == country].groupby('year')['loss_percentage'].mean().reset_index() if is_mean else df[df['country'] == country].groupby('year')['loss_percentage'].size().reset_index()
    return px.bar(result, x='year', y='loss_percentage', title="Top 10 Anos com Menor Perda de Alimento no País")

def generate_graph_production(df, country, is_mean):
    result = df[df['country'] == country].groupby('year')['country_product_prodution'].mean().reset_index() if is_mean else df[df['country'] == country].groupby('year')['country_product_prodution'].size().reset_index()
    return px.bar(result, x='year', y='country_product_prodution', title="Top 10 Anos com Menor Produção de Alimento no País")

def generate_graph_stage(df, country, is_mean):
    result = df[df['country'] == country].dropna(subset=['food_supply_stage']).groupby('year')['loss_percentage'].mean().reset_index() if is_mean else df[df['country'] == country].dropna(subset=['food_supply_stage']).groupby('year')['loss_percentage'].size().reset_index()
    return px.bar(result, x='year', y='loss_percentage', title="Top 10 Anos com Menor Estágio de Fornecimento de Alimento no País")

@callback(
    dash.dependencies.Output('graph-container2', 'children'),
    [dash.dependencies.Input('order-selector_contry', 'value'),
     dash.dependencies.Input('size-selector_contry', 'value'),
     dash.dependencies.Input('stats-selector_contry', 'value'),
     dash.dependencies.Input('contry_selector', 'value')]
)
def update_graph2(order_value_country, size_value_country, stats_value_country, contry_selector):
    if order_value_country == 'crescente':
        if size_value_country == 'top 10':
            if stats_value_country == 'media':
                result_loss = generate_graph_loss(df, contry_selector, True)
                result_production = generate_graph_production(df, contry_selector, True)
                result_stage = generate_graph_stage(df, contry_selector, True)
                return html.Div([
                    dcc.Graph(figure=result_loss, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_production, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_stage, style={'width': '33%', 'display': 'inline-block'})
                ])
            elif stats_value_country == 'instancias':
                result_loss = generate_graph_loss(df, contry_selector, False)
                result_production = generate_graph_production(df, contry_selector, False)
                result_stage = generate_graph_stage(df, contry_selector, False)
                return html.Div([
                    dcc.Graph(figure=result_loss, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_production, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_stage, style={'width': '33%', 'display': 'inline-block'})
                ])
        elif size_value_country == 'top 100':
            if stats_value_country == 'media':
                result_loss = generate_graph_loss(df, contry_selector, True)
                result_production = generate_graph_production(df, contry_selector, True)
                result_stage = generate_graph_stage(df, contry_selector, True)
                return html.Div([
                    dcc.Graph(figure=result_loss, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_production, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_stage, style={'width': '33%', 'display': 'inline-block'})
                ])
            elif stats_value_country == 'instancias':
                result_loss = generate_graph_loss(df, contry_selector, False)
                result_production = generate_graph_production(df, contry_selector, False)
                result_stage = generate_graph_stage(df, contry_selector, False)
                return html.Div([
                    dcc.Graph(figure=result_loss, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_production, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_stage, style={'width': '33%', 'display': 'inline-block'})
                ])
        elif size_value_country == 'all':
            if stats_value_country == 'media':
                result_loss = generate_graph_loss(df, contry_selector, True)
                result_production = generate_graph_production(df, contry_selector, True)
                result_stage = generate_graph_stage(df, contry_selector, True)
                return html.Div([
                    dcc.Graph(figure=result_loss, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_production, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_stage, style={'width': '33%', 'display': 'inline-block'})
                ])
            elif stats_value_country == 'instancias':
                result_loss = generate_graph_loss(df, contry_selector, False)
                result_production = generate_graph_production(df, contry_selector, False)
                result_stage = generate_graph_stage(df, contry_selector, False)
                return html.Div([
                    dcc.Graph(figure=result_loss, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_production, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_stage, style={'width': '33%', 'display': 'inline-block'})
                ])
    elif order_value_country == 'decrescente':
        if size_value_country == 'top 10':
            if stats_value_country == 'media':
                result_loss = generate_graph_loss(df, contry_selector, True)
                result_production = generate_graph_production(df, contry_selector, True)
                result_stage = generate_graph_stage(df, contry_selector, True)
                return html.Div([
                    dcc.Graph(figure=result_loss, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_production, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_stage, style={'width': '33%', 'display': 'inline-block'})
                ])
            elif stats_value_country == 'instancias':
                result_loss = generate_graph_loss(df, contry_selector, False)
                result_production = generate_graph_production(df, contry_selector, False)
                result_stage = generate_graph_stage(df, contry_selector, False)
                return html.Div([
                    dcc.Graph(figure=result_loss, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_production, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_stage, style={'width': '33%', 'display': 'inline-block'})
                ])
        elif size_value_country == 'top 100':
            if stats_value_country == 'media':
                result_loss = generate_graph_loss(df, contry_selector, True)
                result_production = generate_graph_production(df, contry_selector, True)
                result_stage = generate_graph_stage(df, contry_selector, True)
                return html.Div([
                    dcc.Graph(figure=result_loss, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_production, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_stage, style={'width': '33%', 'display': 'inline-block'})
                ])
            elif stats_value_country == 'instancias':
                result_loss = generate_graph_loss(df, contry_selector, False)
                result_production = generate_graph_production(df, contry_selector, False)
                result_stage = generate_graph_stage(df, contry_selector, False)
                return html.Div([
                    dcc.Graph(figure=result_loss, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_production, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_stage, style={'width': '33%', 'display': 'inline-block'})
                ])
        elif size_value_country == 'all':
            if stats_value_country == 'media':
                result_loss = generate_graph_loss(df, contry_selector, True)
                result_production = generate_graph_production(df, contry_selector, True)
                result_stage = generate_graph_stage(df, contry_selector, True)
                return html.Div([
                    dcc.Graph(figure=result_loss, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_production, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_stage, style={'width': '33%', 'display': 'inline-block'})
                ])
            elif stats_value_country == 'instancias':
                result_loss = generate_graph_loss(df, contry_selector, False)
                result_production = generate_graph_production(df, contry_selector, False)
                result_stage = generate_graph_stage(df, contry_selector, False)
                return html.Div([
                    dcc.Graph(figure=result_loss, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_production, style={'width': '33%', 'display': 'inline-block'}),
                    dcc.Graph(figure=result_stage, style={'width': '33%', 'display': 'inline-block'})
                ])
    