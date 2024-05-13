import pandas as pd
import dash
import plotly.graph_objects as go
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import time
import plotly.express as px


df = pd.read_csv("/Users/joaopino/Downloads/acertar/datasets/dataset.csv")

dash.register_page(__name__, path='/world') 

top_products_wasted = df.groupby('product')['loss_percentage'].mean().nlargest(10).sort_values(ascending=True)
fig_top_products_wasted = px.bar(top_products_wasted, y=top_products_wasted.index, x='loss_percentage', 
                                 orientation='h',
                                 title="Top 10 Produtos Mais Desperdiçados",
                                 labels={'loss_percentage': 'Percentagem de Perda (%)'})

fig_top_products_wasted.update_traces(marker_color='green')

for trace in fig_top_products_wasted.data:
    fig_top_products_wasted.add_trace(
        go.Scatter(
            y=trace.y,
            x=trace.x,
            text=trace.y,
            mode='text',
            textposition='middle left',
            showlegend=False
        )
    )

fig_top_products_wasted.update_layout(yaxis={'tickmode': 'array', 'tickvals': [], 'tickangle': -90, 'tickfont': {'color': 'rgb(245, 245, 220)'}},
                                      margin=dict(l=50, r=50, t=50, b=50))

world_loss_media = df.groupby('country')['loss_percentage'].mean().reset_index()
fig_world_loss_media = px.choropleth(world_loss_media, 
                                     locations='country', 
                                     locationmode='country names', 
                                     color='loss_percentage', 
                                     hover_name='country', 
                                     color_continuous_scale='greens',
                                     title='Média de Perda de Alimento por País')

fig_world_loss_media.update_layout(margin=dict(l=50, r=50, t=50, b=50))

top_products_produced = df.groupby('product')['country_product_prodution'].mean().nlargest(10).sort_values(ascending=True)
fig_top_products_produced = px.bar(top_products_produced, y=top_products_produced.index, x='country_product_prodution', 
                                   orientation='h',
                                   title="Top 10 Produtos Mais Produzidos",
                                   labels={'country_product_prodution': 'Produção por País'})

fig_top_products_produced.update_traces(marker_color='green')

for trace in fig_top_products_produced.data:
    fig_top_products_produced.add_trace(
        go.Scatter(
            y=trace.y,
            x=trace.x,
            text=trace.y,
            mode='text',
            textposition='middle left',
            showlegend=False
        )
    )

fig_top_products_produced.update_layout(yaxis={'tickmode': 'array', 'tickvals': [], 'tickangle': -90, 'tickfont': {'color': 'rgb(245, 245, 220)'}},
                                        margin=dict(l=50, r=50, t=50, b=50))
    
layout = html.Div(id='world_page', style={'background-color': 'rgb(240, 240, 240)', 'color': 'rgb(240, 240, 220)'}, children=[
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.H1("World", style={'text-align': 'center', 'background-color': 'rgb(240, 240, 240)', 'color': 'green'}),
        html.Div([
            html.Div([
                html.Div([
                    html.Button("Country", id="country-button", n_clicks=0, style={'background-color': 'green', 'color': 'rgb(240, 240, 240)', 'width': '10vw', 'height' : '2.5vw', 'font-size': '16px', 'border-radius': '8px', 'margin': 'auto'}),
                ]),
                html.Div([
                    html.Button("Product", id="product-button", n_clicks=0, style={'background-color': 'green', 'color': 'rgb(240, 240, 240)', 'width': '10vw', 'height' : '2.5vw', 'font-size': '16px', 'border-radius': '8px', 'margin': 'auto'}),
                ])
            ], style={'width': '50%', 'display': 'flex', 'justify-content': 'space-between', 'margin': 'auto'}),
        ], style={'width': '100%', 'display': 'flex', 'justify-content': 'space-between', 'background-color': 'rgb(240, 240, 240)'}),

        html.Div([
            html.Div([    
                html.Div([
                    dcc.Graph(id='top-products-wasted', figure=fig_top_products_wasted, style={'width': '38vw', 'height': '36vh', 'border': '10px solid rgb(240, 240, 240)'})
                ], style={'width': '100%', 'height': '50%'}),
                html.Div([
                    dcc.Graph(id='top-products-produced', figure=fig_top_products_produced, style={'width': '38vw', 'height': '36vh', 'border': '10px solid rgb(240, 240, 240)'})
                ], style={'width': '100%', 'height': '50%'})
            ], style={'display': 'flex', 'flex-direction': 'column', 'width': '40%', 'height': '100%'}),
            
            html.Div([
                dcc.Graph(id='world-map', figure=fig_world_loss_media, style={'width': '56vw', 'height': '72vh', 'border': '10px solid rgb(240, 240, 240)'})
            ], style={'width': '60%', 'height': '100%', 'border': '10px solid rgb(240, 240, 240)'})
        ], style={'display': 'flex', 'flex-direction': 'row'}),        
    ]),
])
