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

dash.register_page(__name__, path='/world') 

world_loss_media = df.groupby('country')['loss_percentage'].mean().reset_index()
fig_world_loss_media = px.choropleth(world_loss_media, 
                                     locations='country', 
                                     locationmode='country names', 
                                     color='loss_percentage', 
                                     hover_name='country', 
                                     color_continuous_scale='greens',
                                     title='Média de Perda de Alimento por País')

fig_world_loss_media.update_layout(margin=dict(l=50, r=50, t=50, b=50))
    
    
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
                f"{'Country'}", href='/country',className="navbar-body"
            ),
        dcc.Link(
                f"{'Product'}", href='/map',className="navbar-body"
            ),
    ]
)


layout = html.Div(id='world', style={'background-color': 'rgb(240, 240, 240)', 'color': 'rgb(240, 240, 220)'}, children=[
    navbar,
    
    dcc.Location(id='world', refresh=False),
    html.Div([
        html.H1("World", style={'text-align': 'center', 'background-color': 'rgb(240, 240, 240)', 'color': '#EF80A2', 'height' : '3vw', 'line-height': '3vw'}),
        
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
                
                dcc.Dropdown(
                    id='order-selector-product',
                    options=[
                        {'label': 'Crescente', 'value': 'crescente'},
                        {'label': 'Decrescente', 'value': 'decrescente'},
                    ],
                    value='crescente',
                    placeholder="Order",
                    style={'background-color': '#EF80A2', 'color': 'black', 'width': '10vw', 'height' : '2.5vw', 'font-size': '1.2vw', 'border-radius': '12px'}
                ),
                    
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

@callback(
    Output('world-map', 'figure'),
    [Input('year-slider', 'value')]
)
def update_map(selected_year):
    # Filtrar os dados pelo ano selecionado e anos posteriores a 2000
    df_year = df[(df['year'] >= 2000) & (df['year'] == selected_year)]
    
    # Calcular a média de desperdício por país
    world_loss_media = df_year.groupby('country')['loss_percentage'].mean().reset_index()
    
    # Criar o gráfico de mapa
    fig = px.choropleth(
        world_loss_media, 
        locations='country', 
        locationmode='country names', 
        color='loss_percentage', 
        hover_name='country', 
        color_continuous_scale='greens',
        title=f'Desperdício Médio de Alimentos por País em {selected_year}',
        range_color=[0, df['loss_percentage'].max()]
    )
    
    fig.update_layout(
        margin=dict(l=50, r=50, t=50, b=50),
        coloraxis_colorbar=dict(title='Desperdício Médio (%)')
    )
    
    return fig

@callback(
    [Output('top-products-wasted', 'figure'),
     Output('top-products-produced', 'figure')],
    [Input('year-slider', 'value'),
     Input('order-selector-product', 'value')]  # Adicione este Input para capturar a seleção do dropdown
)
def update_bar_charts(selected_year, order):
    # Filtrar os dados pelo ano selecionado e anos posteriores a 2000
    df_year = df[(df['year'] >= 2000) & (df['year'] == selected_year)]
    
    # Calcula as métricas para os gráficos de barras
    if order == 'crescente':
        top_products_wasted = df_year.groupby('product')['loss_percentage'].mean().nlargest(10).sort_values(ascending=True)
        top_products_produced = df_year.groupby('product')['country_product_prodution'].mean().nlargest(10).sort_values(ascending=True)
        
        fig_top_products_wasted = px.bar(top_products_wasted, y=top_products_wasted.index, x='loss_percentage', 
                                    orientation='h',
                                    title="Top 10 Produtos Mais Desperdiçados",
                                    labels={'loss_percentage': 'Percentagem de Perda (%)'})

        fig_top_products_wasted.update_traces(marker_color='#4BB274')

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

        fig_top_products_produced = px.bar(top_products_produced, y=top_products_produced.index, x='country_product_prodution', 
                                    orientation='h',
                                    title="Top 10 Produtos Mais Produzidos",
                                    labels={'country_product_prodution': 'Produção por País'})

        fig_top_products_produced.update_traces(marker_color='#4BB274')

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
    else:
        top_products_wasted = df_year.groupby('product')['loss_percentage'].mean().nsmallest(10).sort_values(ascending=False)
        top_products_produced = df_year.groupby('product')['country_product_prodution'].mean().nsmallest(10).sort_values(ascending=False)
        
        fig_top_products_wasted = px.bar(top_products_wasted, y=top_products_wasted.index, x='loss_percentage', 
                            orientation='h',
                            title="Top 10 Produtos Menos Desperdiçados",
                            labels={'loss_percentage': 'Percentagem de Perda (%)'})

        fig_top_products_wasted.update_traces(marker_color='#4BB274')

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

        fig_top_products_produced = px.bar(top_products_produced, y=top_products_produced.index, x='country_product_prodution', 
                                    orientation='h',
                                    title="Top 10 Produtos Menos Produzidos",
                                    labels={'country_product_prodution': 'Produção por País'})

        fig_top_products_produced.update_traces(marker_color='#4BB274')

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

    return fig_top_products_wasted, fig_top_products_produced