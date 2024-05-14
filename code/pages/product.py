import pandas as pd
import dash
import plotly.graph_objects as go
import dash_ag_grid as dag
from dash import dcc, html, callback, dash_table
from dash.dependencies import Input, Output
import time
import plotly.express as px
import dash_table.FormatTemplate as FormatTemplate

# Define the format template for the loss percentage
percentage_format = FormatTemplate.percentage(2)

dash.register_page(__name__, path='/product') 

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
    dcc.Location(id='product_page', refresh=False),
    
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
                        options=[{'label': str(stage), 'value': str(stage)} for stage in sorted(df["food_supply_stage"].astype(str).dropna().unique())],
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
                            {'label': 'Top 5', 'value': 5},
                            {'label': 'Top 10', 'value': 10},
                            {'label': 'Top 100', 'value': 100},
                        ],
                        value=5,
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
    
    html.Div( className = "product-graphs-wrapper", 
        children=[
        html.Div(className = "product-charts-wrapper",
            children=[
                html.Div(className = "product-top-countries-container",children=[ 
                    dcc.Graph(id='product-top-countries', className='product-top-countries'),
                ]),
                html.Div(className = "product-pieChart-container",children=[ 
                    dcc.Graph(id='product-pieChart', className='product-pieChart'),
                ]),
            ],
        ) ,
        html.Div(className = "product-time-analysis-wrapper",
            children=[
                html.Div(className = "product-waste-time-analysis-container",children=[ 
                    dcc.Graph(id='product-waste-time-analysis', className='product-waste-time-analysis'),
                ]),
                html.Div(className = "product-production-time-analysis-container",children=[ 
                    dcc.Graph(id='product-production-time-analysis', className='product-production-time-analysis'),
                ]),
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


