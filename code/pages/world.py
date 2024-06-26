import pandas as pd
import dash
import plotly.graph_objects as go
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import time
import plotly.express as px

from dash.exceptions import PreventUpdate
from dash import callback_context

dash.register_page(__name__, path='/world') 

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


layout = html.Div(id='world', style={'background-color': 'rgb(240, 240, 240)', 'color': 'rgb(240, 240, 220)'}, children=[
    navbar,
    
    dcc.Location(id='world', refresh=False),
    html.Div([
        html.H1("World", style={'text-align': 'center', 'background-color': 'rgb(240, 240, 240)', 'color': '#EF80A2', 'height' : '3vw', 'line-height': '3vw'}),
        
        html.Button('Start', id='start-button', n_clicks=0, style={'width': '100px', 'height': '30px', 'background-color': '#EF80A2'}),
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
    
    # html.Div(className='landingpage-footer'),
        html.Div([
            html.B("Project organized by João Pino and Miguel Sérgio for “Advanced Data Analysis”class in Universidade de Coimbra"),
        ],className="landingpage-footer-body"),
])

@callback(
    Output('world-map', 'figure'),
    [Input('year-slider', 'value')],
    allow_duplicate=True
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
     Input('order-selector-product', 'value')],  # Adicione este Input para capturar a seleção do dropdown
    allow_duplicate=True
)
def update_bar_charts(selected_year, order):
    # Filtrar os dados pelo ano selecionado e anos posteriores a 2000
    df_year = df[(df['year'] >= 2000) & (df['year'] == selected_year)]
    
    # Calcula as métricas para os gráficos de barras
    if order == 'crescente':
        top_products_wasted = df_year.groupby('product')['loss_percentage'].mean().nlargest(5).sort_values(ascending=True)
        top_products_produced = df_year.groupby('product')['country_product_prodution'].mean().nlargest(5).sort_values(ascending=True)
        
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
        top_products_wasted = df_year.groupby('product')['loss_percentage'].mean().nsmallest(5).sort_values(ascending=False)
        top_products_produced = df_year.groupby('product')['country_product_prodution'].mean().nsmallest(5).sort_values(ascending=False)
        
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

@callback(
    [Output('year-slider', 'value'),
     Output('auto-stepper', 'disabled')],
    [Input('start-button', 'n_clicks'),
     Input('auto-stepper', 'n_intervals')],
    [State('year-slider', 'value'),
     State('auto-stepper', 'disabled')],
    allow_duplicate=True  # Permitir múltiplos callbacks modificando a mesma saída
)
def manage_slider(n_clicks, n_intervals, year_value, interval_disabled):
    ctx = callback_context

    # Determinar qual input disparou o callback (start-button ou auto-stepper)
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'start-button':
        # Lógica para iniciar ou parar
        if n_clicks % 2 == 1:  # Se é ímpar, o usuário quer iniciar
            return (max(year_value, 2000) if year_value < df['year'].max() else 2000, False)
        else:  # Se é par, o usuário quer parar
            return (year_value, True)

    elif trigger_id == 'auto-stepper':
        # Lógica de avanço automático do ano
        if not interval_disabled:
            new_year = year_value + 1 if year_value < df['year'].max() else 2000
            return (new_year, interval_disabled)

    return (year_value, interval_disabled)

