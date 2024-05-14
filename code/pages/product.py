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
    
    html.Div(className="product-filters-headers-wrapper",
        children=[
            html.H1("Select the product for Analysis",className="product-selecter-button-header"),
            html.H1("Filters",className="filers-selecter-button-header"),            
        ]         
    ),
    
    html.Div( className="product-selecter-wrapper", children=[
        
        html.Div(className="product-selecter-button-box", children=[            
            dcc.Dropdown(
                className="product-selecter-dropdown",
                id="product-dropdown",
                options=[{'label': product, 'value': product} for product in df["product"].dropna().unique()],
                value='Cereals, Total',
                clearable=False
            )
        ]),
             
        html.Div(className="product-filter-selecter-dropdown-one-box", children=[            
            dcc.Dropdown(
                    id='product-top-selector',
                    className= "product-filter-selecter-dropdown",
                    options=[
                        {'label': 'Top 5', 'value': 5},
                        {'label': 'Top 10', 'value': 10},
                        {'label': 'Top 100', 'value': 100},
                    ],
                    value=5,
                    placeholder="Order",
                ),
        ]),
            
        html.Div(className="product-filter-selecter-dropdown-two-box", children=[            
            dcc.Dropdown(
                    id='product-order-selector',
                    className= "product-filter-selecter-dropdown",
                    options=[
                        {'label': 'Crescent', 'value': 'crescent'},
                        {'label': 'Decrescent', 'value': 'decrescent'},
                    ],
                    value='crescent',
                    placeholder="Order",
                ),
        ]),
        
    ]),
    html.Div( className = "product-slider-wrapper",
        children = [
        
        html.H1("Time Analysis", className="product-slider-header"),
        
        dcc.Slider(
            id='year-slider',
            className = "product-slider",
            min=2000,
            max=df['year'].max(),
            value=df['year'].min(),
            marks={str(year): str(year) for year in df['year'].unique()},
            step=None
        ),
         
        ],
    ),
    
    html.Div(className = "product-barGraph-wrapper",
        children=[
            html.Div(className = "product-product-barGraph-container",children=[ 
                dcc.Graph(id='product-products-barGraph', className='product-products-barGraph'),
            ]),
            html.Div(className = "product-waste-barGraph-container",children=[ 
                dcc.Graph(id='product-waste-barGraph', className='product-waste-barGraph'),
            ]),
        ],
    ),

    html.Div(className = "product-charts-wrapper", children=[
        html.Div(className = "product-ranking-container",children=[ 
            dcc.Graph(id='product-top-products-barGraph', className='product-products-top-barGraph'),
        ]),
        html.Div(className = "product-pieChart-container",children=[ 
            dcc.Graph(id='product-pieChart', className='product-pieChart'),
        ])
    ])      
])

def generate_production_dataframe_by_product(df, product):
    result = df[df['product'] == product].groupby('year')['country_product_prodution'].mean().reset_index()
    return result

@callback(
    dash.dependencies.Output('product-products-barGraph', 'figure'),
    [dash.dependencies.Input('product-dropdown', 'value'),]
)
def update_production_graph(product):
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
    return fig

def generate_waste_dataframe_by_product(df, product):
    result = df[df['product'] == product].groupby('year')['loss_percentage'].mean().reset_index()
    return result

@callback(
    dash.dependencies.Output('product-waste-barGraph', 'figure'),
    [dash.dependencies.Input('product-dropdown', 'value'),]
)
def update_waste_graph(product):
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
     dash.dependencies.Input('year-slider', 'value'),
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