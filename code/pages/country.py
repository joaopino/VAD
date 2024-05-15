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

dash.register_page(__name__, path='/country') 

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

def generate_world_waste_med_ranked(df):
    filtered_df = df.dropna(subset=['loss_percentage']).groupby('country')['loss_percentage'].mean().reset_index()
    filtered_df['rank'] = filtered_df['loss_percentage'].rank(ascending=True, method='min')
    filtered_df.sort_values(by='rank', inplace=True)
    
    count = 0
    last_rank = 0
    for index, country in filtered_df.iterrows():
        if last_rank == country["rank"]:
            count += 1
        else:
            count = 0
        filtered_df.at[index, "rank"] = country["rank"] + count
        last_rank = country["rank"]
        
    return filtered_df

def get_leaderboard_df(df,country):
    country_loss_df = generate_world_waste_med_ranked(df)
    country_rank = country_loss_df[country_loss_df['country'] == country]['rank'].iloc[0]
    rank_leaderboard = country_loss_df[(country_loss_df['rank'] >= country_rank - 3) & (country_loss_df['rank'] <= country_rank + 3)]
    rank_leaderboard['loss_percentage'] /= 100
    return rank_leaderboard
    

united_states_leaderboard_df = get_leaderboard_df(df,"United States of America")


layout = html.Div(children=[
    dcc.Location(id='contry_page', refresh=False),
    
    navbar,
    
    html.Div(className="country-filters-headers-wrapper",
        children=[
            html.H1("Select the country for Analysis",className="country-selecter-button-header"),
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
                        options=[{'label': country, 'value': country} for country in sorted(df["country"].unique())],
                        value="United States of America",
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
        
        html.Button('Start', id='start-button', n_clicks=0, style={'width': '100px', 'height': '30px', 'background-color': '#EF80A2'}),
        dcc.Interval(id='country-auto-stepper', interval=1*1000, disabled=True),  # Desabilitado inicialmente
        
        dcc.Slider(
            id='country-year-slider',
            min=2000,
            max=df['year'].max(),
            value=df['year'].min(),
            marks={str(year): str(year) for year in df['year'].unique()},
            step=None
        ),
         
        ],
    ),
    
    html.Div( className = "country-graphs-wrapper", 
        children=[
                
        html.Div(className = "country-charts-wrapper",
        children=[
            html.Div(className = "country-ranking-container",children=[ 
                dash_table.DataTable(
                    columns=[{'name': 'Country', 'id': 'country'}, 
                             {'name': 'Loss Percentage', 'id': 'loss_percentage','type': 'numeric', 'format': percentage_format}, 
                             {'name': 'World Ranking', 'id': 'rank'}],
                    data=united_states_leaderboard_df.to_dict("records"),
                    id= "leaderboard-datatable",
                ),
            ], style={'height': '15.5vw', 'width': '35vw', 'marginBottom': '7px'}),
            html.Div(className = "country-pieChart-container",children=[ 
                dcc.Graph(id='country-pieChart', className='country-pieChart'),
            ], style={'height': '15.5vw', 'width': '35vw', 'marginTop': '7px'}),
        ],
    ) ,
        html.Div(className = "country-barGraph-wrapper",
            children=[
                html.Div(className = "country-product-barGraph-container",children=[ 
                    dcc.Graph(id='country-products-barGraph', className='country-products-barGraph'),
                ]),
                html.Div(className = "country-waste-barGraph-container",children=[ 
                    dcc.Graph(id='country-waste-barGraph', className='country-waste-barGraph'),
                ]),
            ],
        ) ,
        ]  
    ),
    #Footer
    # html.Div(className='landingpage-footer'),
    # html.Div([
    #     html.B("Project organized by João Pino and Miguel Sérgio for “Advanced Data Analysis”class in Universidade de Coimbra"),
    # ],className="landingpage-footer-body"),       
])


def generate_graph_stage(df, country, is_mean):
    result = df[df['country'] == country].dropna(subset=['food_supply_stage']).groupby('year')['loss_percentage'].mean().reset_index() if is_mean else df[df['country'] == country].dropna(subset=['food_supply_stage']).groupby('year')['loss_percentage'].size().reset_index()
    return px.bar(result, x='year', y='loss_percentage', title="Top 10 Anos com Menor Estágio de Fornecimento de Alimento no País")

def generate_waste_dataframe_by_country(df, country, is_mean):
    result = df[df['country'] == country].groupby('year')['loss_percentage'].mean().reset_index() if is_mean else df[df['country'] == country].groupby('year')['loss_percentage'].size().reset_index()
    return result

@callback(
    dash.dependencies.Output('country-waste-barGraph', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value'),
     dash.dependencies.Input('country-year-slider', 'value')]
)
def update_waste_graph(country, selected_year):
    #Country -> Name of the country
    #top_flag -> Flag that can be "top5","top10","top100"
    #order -> Flag tha can be "crescent"
    
    filtered_df = generate_waste_dataframe_by_country(df,country,True)
    filtered_df = filtered_df[(filtered_df['year'] >= 2000)]
    
    fig = go.Figure(
        data=[go.Scatter(x=filtered_df['year'], y=filtered_df['loss_percentage'], mode="lines+markers", marker_color='#4BB274')],
        layout=dict(
            margin=dict(b=50),
            title=dict(text=f"Time Analysis of Wasted Food in {country}"),
            title_font_color='black',
            xaxis_title='Year',
            yaxis_title='Percentage of food wasted',
            plot_bgcolor='#FFF9FB',
            paper_bgcolor='#FFF9FB',
            xaxis=dict(gridcolor='rgb(220, 220, 220)'), 
            yaxis=dict(gridcolor='rgb(220, 220, 220)'),
        )
    )
    
    fig.add_vline(x=selected_year, line_dash="dash", line_color="red")
    
    return fig

def generate_production_dataframe_by_country(df, country, is_mean):
    result = df[df['country'] == country].groupby('year')['country_product_prodution'].mean().reset_index() if is_mean else df[df['country'] == country].groupby('year')['country_product_prodution'].size().reset_index()
    return result
@callback(
    dash.dependencies.Output('country-products-barGraph', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value'),
     dash.dependencies.Input('country-year-slider', 'value')]
)
def update_production_graph(country, selected_year):
    #Country -> Name of the country
    #top_flag -> Flag that can be "top5","top10","top100"
    #order -> Flag tha can be "crescent"
    
    filtered_df = generate_production_dataframe_by_country(df,country,True)
    filtered_df = filtered_df[(filtered_df['year'] >= 2000)]
    
    fig = go.Figure(
        data=[go.Scatter(x=filtered_df['year'], y=filtered_df['country_product_prodution'], mode="lines+markers", marker_color='#4BB274')],
        layout=dict(
            margin=dict(b=50),
            title=dict(text=f"Time Analysis of Food Production in {country}"),
            title_font_color='black',
            xaxis_title='Year',
            yaxis_title='Food Produced',
            plot_bgcolor='#FFF9FB',
            paper_bgcolor='#FFF9FB',
            xaxis=dict(gridcolor='rgb(220, 220, 220)'), 
            yaxis=dict(gridcolor='rgb(220, 220, 220)'),
        )
    )
    
    fig.add_vline(x=selected_year, line_dash="dash", line_color="red")
    
    return fig

@callback(
    dash.dependencies.Output('leaderboard-datatable', 'data'),
    [dash.dependencies.Input('country-dropdown', 'value')]
)
def update_leaderboard(country):
    rank_leaderboard = get_leaderboard_df(df, country)
    # Convert DataFrame to list of dictionaries
    leaderboard_data = rank_leaderboard.to_dict('records')
    return leaderboard_data

def get_top_chain_by_country(df, collumn, top, country, year,crescent):
    filtered_df = df[ df['food_supply_stage'] != "Whole supply chain"]
    filtered_df = filtered_df[ filtered_df['country'] == country]
    
    #1961 does not have any data, but is the default stating point on the slider value
    
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
    for index, country in food_loss_product.iterrows():
        if last_rank == country["rank"]:
            count += 1
        else:
            count = 0
        food_loss_product.at[index, "rank"] = country["rank"] + count
        last_rank = country["rank"]
        
    food_loss_product = food_loss_product.head(top)
    sum_loss = food_loss_product[collumn].sum()
    
    food_loss_product['top_percentage'] = (food_loss_product[collumn] / sum_loss)

    
    return food_loss_product

@callback(
     dash.dependencies.Output('country-pieChart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value'),
     dash.dependencies.Input('country-year-slider', 'value'),
     dash.dependencies.Input('country-top-selector', 'value'),
     dash.dependencies.Input('country-order-selector', 'value'),],
    allow_duplicate=True  # Permitir múltiplos callbacks modificando a mesma saída
)
def update_leaderboard(country,year,top,crescent):
    
    top_df = get_top_chain_by_country(df,"loss_percentage",top,country,year,crescent!="crescent")
    
    fig = px.pie(top_df,
                 values = top_df['loss_percentage'],
                 names = top_df['food_supply_stage'], 
                 hole=.3)
    aux = "food loss in the chains of "
    if(crescent == "crescent"):
        title = "Biggest "+aux + country
    else:
        title = "Lowest "+aux + country 
    fig.update_layout(
    title=title
    )
    return fig
   
@callback(
    Output('leaderboard-datatable', 'style_data_conditional'),
    [Input('country-dropdown', 'value')]
)
def highlight_selected_country(selected_country):
    return [
        {
            'if': {'filter_query': '{{country}} = "{}"'.format(selected_country)},
            'backgroundColor': '#FAD5E0',  # Cor de realce
            'color': 'black'  # Cor do texto na linha realçada
        }
    ]
    
@callback(
    [Output('country-year-slider', 'value'),
     Output('country-auto-stepper', 'disabled')],
    [Input('start-button', 'n_clicks'),
     Input('country-auto-stepper', 'n_intervals')],
    [State('country-year-slider', 'value'),
     State('country-auto-stepper', 'disabled')],
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
        
    elif trigger_id == 'country-auto-stepper':
        if not interval_disabled:
            new_year = year_value + 1 if year_value < df['year'].max() else 2000
            return (new_year, interval_disabled)
        
    return (year_value, interval_disabled)