import pandas as pd
import dash
import plotly.graph_objects as go
from dash import dcc, html, callback
from dash.dependencies import Input, Output

dash.register_page(__name__, path='/') 
    
colors = {
    'background' : '#FFF9FB'
}

    
layout = html.Div([
     html.Div([
        html.H1("Food", className="init-header-food"),
        html.H1("Waste", className="init-header-waste"),
    ]),
    
    #Counter
    html.Div(id='counter-div', className='counter-div', style={'fontFamily': 'Manjari Bold, sans serif', 'textAlign': 'center', 'fontSize': '196px'}),

    
    #Texte bellow counter
    html.Div([
        html.B(" Tons of food were wasted from the 1st of January until the 31st of March 2024", 
               style={'textAlign': 'center', 'fontSize': 20, 'font-family':'jsMas','margin-top': '20px'})
    ], style={'textAlign': 'center'}),
    
    # html.Div([
    #     html.Div([
    #         dcc.Link(
    #             f"{'World'}", href='/map'
    #         ),
    #     ], className='botton margin'),
    #     html.Div([
    #         dcc.Link(
    #             f"{'Country'}", href='/grafic'
    #         ),
    #     ], className='botton margin'),
    #     html.Div([
    #         dcc.Link(
    #             f"{'Year'}", href='/stats'
    #         ),
    #     ], className='botton margin'),
    # ], className='botton-init'),
    # html.Div([
    #     html.Img(src='/assets/logo-init.png'),     
    # ], className='init'),
    
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