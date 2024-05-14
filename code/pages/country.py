import pandas as pd
import dash
import plotly.graph_objects as go
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import time
import plotly.express as px

dash.register_page(__name__, path='/country') 

option = 1
if option == 1:
    df = pd.read_csv("/Users/joaopino/1.Principal/2Semester/VAD/Project/datasets/dataset.csv")
else:
    df = pd.read_csv("C:/Users/narig/OneDrive/Ambiente de Trabalho/VAD - Visualização Avançada de Dados/Projeto_final/VAD/datasets/dataset.csv")


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
                f"{'Product'}", href='/product',className="navbar-body"
            ),
    ]
)


layout = html.Div(children=[
    dcc.Location(id='contry_page', refresh=False),
    
    navbar,
    
    html.Div(className="country-filters-headers-wrapper",
        children=[
            html.H1("Select the product for Analysis",className="country-selecter-button-header"),
            html.H1("Filters",className="filers-selecter-button-header"),            
        ]         
    ),
    
    
    
    
    html.Div( className="country-selecter-wrapper",
        children=[
            html.Div(className="country-selecter-button-box",
            children=[            
                dcc.Dropdown(
                        className= "country-selecter-dropdown",
                        id="country-dropdown",
                        options=[{'label': country, 'value': country} for country in sorted(df["country"].unique())],
                        value=sorted(df["country"].unique())[2],
                        clearable=False,
                    ),
            ]
            ),
             
            html.Div(className="country-filter-selecter-dropdown-one-box",
            children=[            
                dcc.Dropdown(
                        id='order-selector_contry',
                        className= "country-filter-selecter-dropdown",
                        options=[
                            {'label': 'Top 5', 'value': 'top5'},
                            {'label': 'Top 10', 'value': 'top10'},
                            {'label': 'Top 100', 'value': 'top100'},
                        ],
                        value='top5',
                        placeholder="Order",
                    ),
            ]
            ),
            
            html.Div(className="country-filter-selecter-dropdown-two-box",
            children=[            
                dcc.Dropdown(
                        id='order-selector_contry',
                        className= "country-filter-selecter-dropdown",
                        options=[
                            {'label': 'Crescent', 'value': 'crescent'},
                            {'label': 'Decrescent', 'value': 'decrescent'},
                        ],
                        value='crescent',
                        placeholder="Order",
                    ),
            ]
            ),
        ],
    ),
    
    html.Div( className = "country-slider-wrapper",
        children = [
        
        html.H1("Time Analysis", className="country-slider-header"),
        
        dcc.Slider(
            id='year-slider',
            className = "country-slider",
            min=2000,
            max=df['year'].max(),
            value=df['year'].min(),
            marks={str(year): str(year) for year in df['year'].unique()},
            step=None
        ),
         
        ],
    ),
    
    html.Div( className = "country-graphs-wrapper", 
        children=[
                
        html.Div(className = "country-charts-wrapper",
        children=[
            html.Div(className = "country-ranking-countainer",children=[ 
                                                                        
            ]),
            html.Div(className = "country-pieChart-container",children=[ 
                #dcc.Graph(id='country-pieChart', className='country-pieChart'),
            ]),
        ],
    ) ,
        html.Div(className = "country-barGraph-wrapper",
            children=[
                html.Div(className = "country-product-barGraph-container",children=[ 
                    dcc.Graph(id='country-products-barGraph', className='country-products-barGraph'),
                ]),
                html.Div(className = "country-waste-barGraph-container",children=[ 
                    dcc.Graph(id='country-waste-barGraph', className='country-waste-barGraph'),
                ])
            ],
        ) ,
        ]  
    ),
    #Footer
    html.Div(className='landingpage-footer'),
    html.Div([
        html.B("Project organized by João Pino and Miguel Sérgio for “Advanced Data Analysis”class in Universidade de Coimbra"),
    ],className="landingpage-footer-body"),       
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
    
    


