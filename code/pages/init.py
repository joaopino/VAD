import pandas as pd
import dash
import plotly.graph_objects as go
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

dash.register_page(__name__, path='/') 
    
    
navbar = html.Nav(
    className="navbar navbar-expand navbar-light bg-light",
    children=[
        html.A(className="navbar-anchor", href="#"),
        dcc.Link(
                f"{'World'}", href='/world',className="landingpage-navbar-world"
            ),
        dcc.Link(
                f"{'Country'}", href='/country',className="landingpage-navbar-country"
            ),
        dcc.Link(
                f"{'Product'}", href='/product',className="landingpage-navbar-product"
            ),
    ]
)
  
layout = html.Div([
    navbar,
    
     html.Div([
        html.H1("Food", className="init-header-food"),
        html.H1("Waste", className="init-header-waste"),
    ]),
    
    #Counter
    html.Div(id='counter-div', className='landingpage-counter'),
    html.Div([
        html.B("Tons of food that were registered as waste since the 1st of January of 2024"),
    ],className="landingpage-counter-text"),
    
    
    #Footer
    html.Div(className='landingpage-footer'),
    
    
    html.Div([
        html.B("Project organized by João Pino and Miguel Sérgio for “Advanced Data Analysis”class in Universidade de Coimbra"),
    ],className="landingpage-footer-body"),
    
    #Counter Interval calculator
    dcc.Interval(
            id='interval-component',
            interval=1*300,  # in milliseconds
            n_intervals=0
        )
],)

@callback(
    Output('counter-div', 'children'),
    Input('interval-component', 'n_intervals')
)

#
def update_counter(n_intervals):
    return "{:,}".format(5227545550 + n_intervals)