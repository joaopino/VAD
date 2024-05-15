import pandas as pd
import dash
import plotly.graph_objects as go
import dash_ag_grid as dag
from dash import dcc, html, callback, dash_table
from dash.dependencies import Input, Output, State
import time
import plotly.express as px
import dash_table.FormatTemplate as FormatTemplate

from dash.exceptions import PreventUpdate
from dash import callback_context

# Define the format template for the loss percentage
percentage_format = FormatTemplate.percentage(2)

dash.register_page(__name__, path='/product') 

option = 0
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
                        id="product-dropdown",
                        options=[{'label': product, 'value': product} for product in df["product"].dropna().unique()],
                        value='Potatoes',
                        clearable=False,
                    ),
            ]
            ),
             
            html.Div(className="country-filter-selecter-dropdown-one-box",
            children=[            
                dcc.Dropdown(
                        id='product-top-selector',
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
                        id='product-order-selector',
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
        
        html.Button('Start', id='start-button', n_clicks=0, style={'width': '100px', 'height': '30px', 'background-color': '#EF80A2'}),
        dcc.Interval(id='product-auto-stepper', interval=1*1000, disabled=True),  # Desabilitado inicialmente
        
        dcc.Slider(
            id='product-year-slider',
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
                ], style={'height': '15.5vw', 'width': '35vw', 'marginBottom': '7px'}),
                html.Div(className = "product-pieChart-container",children=[ 
                    dcc.Graph(id='product-pieChart', className='product-pieChart'),
                ], style={'height': '15.5vw', 'width': '35vw', 'marginBottom': '7px'}),
            ],
        ) ,
        html.Div(className = "product-time-analysis-wrapper",
            children=[
                html.Div(className = "product-waste-time-analysis-container",children=[ 
                    dcc.Graph(id='product-waste-barGraph', className='product-waste-time-analysis'),
                ]),
                html.Div(className = "product-production-time-analysis-container",children=[ 
                    dcc.Graph(id='product-products-barGraph', className='product-production-time-analysis'),
                ]),
            ],
        ) ,
        ]  
    ),
    
    
    # #Footer
    # html.Div(className='landingpage-footer'),
    # html.Div([
    #     html.B("Project organized by João Pino and Miguel Sérgio for “Advanced Data Analysis”class in Universidade de Coimbra"),
    # ],className="landingpage-footer-body"),       
])

def generate_production_dataframe_by_product(df, product):
    result = df[df['product'] == product].groupby('year')['country_product_prodution'].mean().reset_index()
    return result

@callback(
    dash.dependencies.Output('product-products-barGraph', 'figure'),
    [dash.dependencies.Input('product-dropdown', 'value'),
     dash.dependencies.Input('product-year-slider', 'value')]
)
def update_production_graph(product, selected_year):
    filtered_df = generate_production_dataframe_by_product(df,product)
    filtered_df = filtered_df[(filtered_df['year'] >= 2000)]
    
    fig = go.Figure(
        data=[go.Scatter(x=filtered_df['year'], y=filtered_df['country_product_prodution'], mode="lines+markers", marker_color='#4BB274')],
        layout=dict(
            margin=dict(b=50),
            title=dict(text=f"Time Analysis of Food Production of {product}"),
            title_font_color='black',
            xaxis_title='Year',
            yaxis_title='Food Produced',
            plot_bgcolor='#FFF9FB',
            paper_bgcolor='#FFF9FB',
            xaxis=dict(gridcolor='rgb(220, 220, 220)'), 
            yaxis=dict(gridcolor='rgb(220, 220, 220)'),
        )
    )
    
    # Add a marker for the selected year
    fig.add_vline(x=selected_year, line_dash="dash", line_color="red")
    
    return fig

def generate_waste_dataframe_by_product(df, product):
    result = df[df['product'] == product].groupby('year')['loss_percentage'].mean().reset_index()
    return result

@callback(
    dash.dependencies.Output('product-waste-barGraph', 'figure'),
    [dash.dependencies.Input('product-dropdown', 'value'),
     dash.dependencies.Input('product-year-slider', 'value')]
)
def update_waste_graph(product, selected_year):
    filtered_df = generate_waste_dataframe_by_product(df,product)
    filtered_df = filtered_df[(filtered_df['year'] >= 2000)]
    
    fig = go.Figure(
        data=[go.Scatter(x=filtered_df['year'], y=filtered_df['loss_percentage'], mode="lines+markers", marker_color='#4BB274')],
        layout=dict(
            margin=dict(b=50),
            title=dict(text=f"Time Analysis of Wasted Food of {product}"),
            title_font_color='black',
            xaxis_title='Year',
            yaxis_title='Percentage of food wasted',
            plot_bgcolor='#FFF9FB',
            paper_bgcolor='#FFF9FB',
            xaxis=dict(gridcolor='rgb(220, 220, 220)'), 
            yaxis=dict(gridcolor='rgb(220, 220, 220)'),
        )
    )
    
    # Add a marker for the selected year
    fig.add_vline(x=selected_year, line_dash="dash", line_color="red")
    
    return fig

def get_top_chain_by_product(df, collumn, top, product, year,crescent):
    filtered_df = df[ df['food_supply_stage'] != "Whole supply chain"]
    filtered_df = filtered_df[ filtered_df['product'] == product]    
    if year != 1961:
        filtered_df = filtered_df[ filtered_df['year'] == year]
    else:
        food_loss_product = filtered_df.groupby('year')[collumn].sum().reset_index()    
        
    food_loss_product = filtered_df.groupby('food_supply_stage')[collumn].sum().reset_index()    
    food_loss_product = food_loss_product[food_loss_product[collumn] != 0]
    
    food_loss_product['rank'] = food_loss_product[collumn].rank(ascending=crescent, method='min')
    food_loss_product.sort_values(by='rank', inplace=True)
    
    count = 0
    last_rank = 0
    for index, product in food_loss_product.iterrows():
        if last_rank == product["rank"]:
            count += 1
        else:
            count = 0
        food_loss_product.at[index, "rank"] = product["rank"] + count
        last_rank = product["rank"]
        
    food_loss_product = food_loss_product.head(top)
    sum_loss = food_loss_product[collumn].sum()
    
    food_loss_product['top_percentage'] = (food_loss_product[collumn] / sum_loss)

    
    return food_loss_product

@callback(
     dash.dependencies.Output('product-pieChart', 'figure'),
    [dash.dependencies.Input('product-dropdown', 'value'),
     dash.dependencies.Input('product-year-slider', 'value'),
     dash.dependencies.Input('product-top-selector', 'value'),
     dash.dependencies.Input('product-order-selector', 'value'),]
)
def update_leaderboard(product,year,top,crescent):
    
    top_df = get_top_chain_by_product(df,"loss_percentage",top,product,year,crescent!="crescent")
    
    fig = px.pie(top_df,
                 values = top_df['loss_percentage'],
                 names = top_df['food_supply_stage'], 
                 hole=.3)
    aux = "food loss in the chains of "
    if(crescent == "crescent"):
        title = "Biggest "+aux + product
    else:
        title = "Lowest "+aux + product 
    fig.update_layout(
    title=title
    )
    return fig

def get_top_countries_by_product(df, product, year, top, crescent):
    filtered_df = df[df['product'] == product]
    if year != 1961:
        filtered_df = filtered_df[filtered_df['year'] == year]

    filtered_df = filtered_df.groupby('country')['loss_percentage'].mean().reset_index()
    filtered_df.sort_values(by='loss_percentage', ascending=crescent, inplace=True)
    top_countries = filtered_df.head(top)

    return top_countries

@callback(
    Output('product-top-countries', 'figure'),
    [
        Input('product-dropdown', 'value'),
        Input('product-year-slider', 'value'),
        Input('product-top-selector', 'value'),
        Input('product-order-selector', 'value'),
    ],
)
def update_top_countries_graph(product, year, top, crescent):
    top_countries_df = get_top_countries_by_product(df, product, year, top, crescent != "crescent")

    fig = go.Figure(
        data=[go.Bar(x=top_countries_df['country'], y=top_countries_df['loss_percentage'], marker_color='#4BB274')],
        layout=dict(
            margin=dict(b=50),
            title=dict(text=f"Top {top} Countries with Highest Food Waste for {product}"),
            title_font_color='black',
            xaxis_title='Country',
            yaxis_title='Percentage of Food Wasted',
            plot_bgcolor='#FFF9FB',
            paper_bgcolor='#FFF9FB',
            xaxis=dict(gridcolor='rgb(220, 220, 220)'),
            yaxis=dict(gridcolor='rgb(220, 220, 220)'),
        )
    )
    
    return fig

@callback(
    [Output('product-year-slider', 'value'),
     Output('product-auto-stepper', 'disabled')],
    [Input('start-button', 'n_clicks'),
     Input('product-auto-stepper', 'n_intervals')],
    [State('product-year-slider', 'value'),
     State('product-auto-stepper', 'disabled')],
    allow_duplicate=True  # Permitir múltiplos callbacks modificando a mesma saída
)
def manage_slider(n_clicks, n_intervals, year_value, interval_disabled):
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'start-button':
        if n_clicks % 2 == 1:  # Se é ímpar, o usuário quer iniciar        
            return (max(year_value, 2000) if year_value < df['year'].max() else 2000, False)
        else:
            return (year_value, True)
        
    elif trigger_id == 'product-auto-stepper':
        if not interval_disabled:
            new_year = year_value + 1 if year_value < df['year'].max() else 2000
            return (new_year, interval_disabled)
        
    return (year_value, interval_disabled)