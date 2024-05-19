import pandas as pd
import dash
import plotly.graph_objects as go
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import time
import plotly.express as px

from dash.exceptions import PreventUpdate
from dash import callback_context

dash.register_page(__name__, path='/world2') 

option = 1
if option == 1:
    df = pd.read_csv("/Users/joaopino/1.Principal/2Semester/VAD/Project/datasets/dataset.csv")
else:
    df = pd.read_csv("C:/Users/narig/OneDrive/Ambiente de Trabalho/VAD - Visualização Avançada de Dados/Projeto_final/VAD/datasets/dataset.csv")

navbar = html.Nav(
    
    className="navbar navbar-expand navbar-light bg-light",
    children=[
        html.A(className="navbar-anchor", href="#"),
        
        dcc.Link(html.Span("Food", className="navbar-icon-Food"), href='/'),
        dcc.Link(html.Span("Waste", className="navbar-icon-Waste"), href='/'),
        dcc.Link(
                f"{'World'}", href='/world',className="landingpage-navbar-body"
            ),
        dcc.Link(
                f"{'Country'}", href='/country',className="landingpage-navbar-body"
            ),
        dcc.Link(
                f"{'Product'}", href='/product',className="landingpage-navbar-body"
            ),
    ]
)

world_loss_media = df.groupby('country')['loss_percentage'].mean().reset_index()
fig_world_loss_media = px.choropleth(world_loss_media, 
                                     locations='country', 
                                     locationmode='country names', 
                                     color='loss_percentage', 
                                     hover_name='country', 
                                     color_continuous_scale='greens',
                                     title='Média de Perda de Alimento por País')

fig_world_loss_media.update_layout(margin=dict(l=50, r=50, t=50, b=50))


layout = html.Div(children=[
    
    navbar,
    dcc.Location(id='world2', refresh=False),
    
    html.Div([
        
        dcc.Interval(id='auto-stepper', interval=1*1000, disabled=True),  # Desabilitado inicialmente
        
        dcc.Slider(
            id='year-slider',
            min=2000,
            max=df['year'].max(),
            value=2000,
            marks={str(year): str(year) for year in df['year'].unique()},
            step=None
        ),
        
        html.Div([
            
            html.Div([
                
                html.Div([
                    dcc.Dropdown(
                        id='order-selector-product',
                        options=[
                            {'label': 'Top 5', 'value': 'crescente'},
                            {'label': 'Bottom 5', 'value': 'decrescente'},
                        ],
                        value='crescente',
                        placeholder="Order",
                        style={'background-color': '#EF80A2', 'color': 'black', 'width': '10vw', 'height' : '2.5vw', 'font-size': '1.2vw', 'border-radius': '12px'}
                    ),
                ], style={'margin-left': '0.5vw'}),
                    
                html.Div([
                    dcc.Graph(id='top-products-wasted', style={'width': '38vw', 'height': '29vh', 'border': '10px solid rgb(240, 240, 240)'})
                ], style={'width': '100%', 'height': '50%'}),
                html.Div([
                    dcc.Graph(id='top-products-produced', style={'width': '38vw', 'height': '29vh', 'border': '10px solid rgb(240, 240, 240)'})
                ], style={'width': '100%', 'height': '50%'})
                
            ], style={'display': 'flex', 'flex-direction': 'column', 'width': '40%', 'height': '100%'}),
            
            html.Div([
                dcc.Graph(id='world-map', figure=fig_world_loss_media, style={'border': '10px solid rgb(240, 240, 240)', 'margin-top': '38px', 'height': '61vh'}),
            ], style={'width': '60%', 'height': '100%'})
            
        ], style={'display': 'flex', 'flex-direction': 'row'}),        
    ]),
    
    html.Div(className='landingpage-footer'),
        html.Div([
            html.B("Project organized by João Pino and Miguel Sérgio for “Advanced Data Analysis”class in Universidade de Coimbra"),
        ],className="landingpage-footer-body"),
])

