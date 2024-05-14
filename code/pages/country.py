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
                        value="United States of America",
                        clearable=False,
                    ),
            ]
            ),
             
            html.Div(className="country-filter-selecter-dropdown-one-box",
            children=[            
                dcc.Dropdown(
                        id='country-top-selector',
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
                        id='country-order-selector',
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
                dcc.Graph(id='country-pieChart', className='country-pieChart'),
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



def generate_graph_stage(df, country, is_mean):
    result = df[df['country'] == country].dropna(subset=['food_supply_stage']).groupby('year')['loss_percentage'].mean().reset_index() if is_mean else df[df['country'] == country].dropna(subset=['food_supply_stage']).groupby('year')['loss_percentage'].size().reset_index()
    return px.bar(result, x='year', y='loss_percentage', title="Top 10 Anos com Menor Estágio de Fornecimento de Alimento no País")

def generate_waste_dataframe_by_country(df, country, is_mean):
    result = df[df['country'] == country].groupby('year')['loss_percentage'].mean().reset_index() if is_mean else df[df['country'] == country].groupby('year')['loss_percentage'].size().reset_index()
    return result
@callback(
    dash.dependencies.Output('country-waste-barGraph', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value'),]
)
def update_waste_graph(country):
    #Country -> Name of the country
    #top_flag -> Flag that can be "top5","top10","top100"
    #order -> Flag tha can be "crescent"
    
    filtered_df = generate_waste_dataframe_by_country(df,country,True)
    filtered_df = filtered_df[(filtered_df['year'] >= 2000)]
    
    fig = go.Figure(
        data=[go.Scatter(x=filtered_df['year'], y=filtered_df['loss_percentage'], mode="lines+markers", marker_color='#4BB274')],
        layout=dict(
            margin=dict(b=50),
            title=dict(text=f"Time Analysis of Wasted Food in {country}"),
            title_font_color='black',
            xaxis_title='Year',
            yaxis_title='Percentage of food wasted',
            plot_bgcolor='#FFF9FB',
            paper_bgcolor='#FFF9FB',
            xaxis=dict(gridcolor='rgb(220, 220, 220)'), 
            yaxis=dict(gridcolor='rgb(220, 220, 220)'),
        )
    )
    return fig

def generate_production_dataframe_by_country(df, country, is_mean):
    result = df[df['country'] == country].groupby('year')['country_product_prodution'].mean().reset_index() if is_mean else df[df['country'] == country].groupby('year')['country_product_prodution'].size().reset_index()
    return result
@callback(
    dash.dependencies.Output('country-products-barGraph', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value'),]
)
def update_production_graph(country):
    #Country -> Name of the country
    #top_flag -> Flag that can be "top5","top10","top100"
    #order -> Flag tha can be "crescent"
    
    filtered_df = generate_production_dataframe_by_country(df,country,True)
    filtered_df = filtered_df[(filtered_df['year'] >= 2000)]
    
    fig = go.Figure(
        data=[go.Scatter(x=filtered_df['year'], y=filtered_df['country_product_prodution'], mode="lines+markers", marker_color='#4BB274')],
        layout=dict(
            margin=dict(b=50),
            title=dict(text=f"Time Analysis of Food Production in {country}"),
            title_font_color='black',
            xaxis_title='Year',
            yaxis_title='Food Produced',
            plot_bgcolor='#FFF9FB',
            paper_bgcolor='#FFF9FB',
            xaxis=dict(gridcolor='rgb(220, 220, 220)'), 
            yaxis=dict(gridcolor='rgb(220, 220, 220)'),
        )
    )
    return fig
