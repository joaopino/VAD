import pandas as pd
import dash
import plotly.graph_objects as go
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import time
import plotly.express as px

option = 1
if option == 1:
    df = pd.read_csv("/Users/joaopino/1.Principal/2Semester/VAD/Project/datasets/dataset.csv")
else:
    df = pd.read_csv("C:/Users/narig/OneDrive/Ambiente de Trabalho/VAD - Visualização Avançada de Dados/Projeto_final/VAD/datasets/dataset.csv")
    

dash.register_page(__name__, path='/product')

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

layout = html.Div(id='product', style={'background-color': 'rgb(240, 240, 240)', 'color': 'rgb(240, 240, 220)'}, children=[
    navbar,
    
    dcc.Location(id='product', refresh=False),
    html.Div([
        
    ])
])
