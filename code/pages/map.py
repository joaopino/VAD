import pandas as pd
import dash
import plotly.graph_objects as go
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import time


#df = pd.read_csv("../../datasets/dataset.csv")

#df

# dash.register_page(__name__, path='/map') 

# anos = sorted(df['Year'].unique())

# slider_layout = html.Div([
#     html.Div(id='slider-container', children=[
#         html.Button("Play", id="play-button", className='botton-play'),
#         html.Button("Pause", id="pause-button", className='botton-play', disabled=True),
#         dcc.Slider(
#             id='year-slider',
#             min=min(anos),
#             max=max(anos),
#             value=min(anos),  # Começa no primeiro ano da lista
#             marks={str(ano): str(ano) for ano in anos},
#             step=None,
#             className="scale"
#         )
#     ], className='line-scale'),
#     dcc.Interval(id='interval', interval=1000, disabled=True)  # Intervalo de atualização a cada segundo
# ])

# @callback(
#     Output('interval', 'disabled'),
#     [Input('play-button', 'n_clicks'),
#      Input('pause-button', 'n_clicks')]
# )
# def control_interval(play_clicks, pause_clicks):
#     if play_clicks and play_clicks > (pause_clicks or 0):
#         return False
#     else:
#         return True

# @callback(
#     Output('play-button', 'disabled'),
#     Output('pause-button', 'disabled'),
#     [Input('play-button', 'n_clicks'),
#      Input('pause-button', 'n_clicks')]
# )
# def control_buttons(play_clicks, pause_clicks):
#     if play_clicks and play_clicks > (pause_clicks or 0):
#         return True, False
#     else:
#         return False, True

# @callback(
#     Output('year-slider', 'value'),
#     [Input('interval', 'n_intervals')]
# )
# def update_slider(n_intervals):
#     if n_intervals is None:
#         return min(anos)  # Retorna o primeiro ano da lista
#     year_index = n_intervals % len(anos)
#     return anos[year_index]

# @callback(
#     Output('interval', 'max_intervals'),
#     [Input('play-button', 'n_clicks')]
# )
# def set_max_intervals(n_clicks):
#     if n_clicks:
#         return n_clicks * len(anos)
#     else:
#         return dash.no_update

# mapa_layout = dcc.Graph(
#     id='crime-map',
#     className='map-pos'
# )

# bar_layout = html.Div([
#     dcc.Graph(id='top-5-countries-highest-crime-rate-graph', className='graph-top'),
#     dcc.Graph(id='crime-rate-graph', className='graph-map')
# ])

# layout = html.Div([
#      html.Div([
#         html.Div([
#             html.A(
#                 html.Img(src='/assets/logo.png'), 
#                 href='/'
#             )
#         ], className='logo'),
#         html.Div([
#             html.Div([
#                 dcc.Link(
#                     f"{'Country'}", href='/grafic'
#                 ),
#             ], className='botton'),
#             html.Div([
#                 dcc.Link(
#                     f"{'Year'}", href='/stats'
#                 ),
#             ], className='botton'),
#         ], className='botton-loc'),
#     ], className='navbar'),
#     dcc.Location(id='url', refresh=False),
#     html.Div([
#         bar_layout,
#         html.Div([mapa_layout]),
#     ],
#     className="line2"),
#     html.Div([slider_layout])
# ],)

# @callback(
#     [Output('crime-map', 'figure'),
#      Output('crime-rate-graph', 'figure'),
#      Output('top-5-countries-highest-crime-rate-graph', 'figure')],
#     [Input('year-slider', 'value')]
# )
# def update_graph(year):
#     data = [go.Choropleth(
#         z=df[df['Year'] == year]['Criminality Rate'],
#         locations=df[df['Year'] == year]['Country Code'],
#         text=df[df['Year'] == year]['Country'],
#         colorscale='YlOrRd',
#         autocolorscale=False,
#         reversescale=False,
#         marker_line_color='darkgray',
#         marker_line_width=0.1,
#         hovertemplate='<b>%{text}</b><br>' +
#                       'Crime rate: %{z} per 100K people<br>' +
#                       'Criminal rank: %{customdata}th place<br>' +
#                       'Year: ' + str(year),
#         customdata=df[df['Year'] == year]['Criminality Rank'],
#         colorbar_title='Rate',
#         showscale=True,
#         name='',
#         hoverlabel=dict(font=dict(family='Poppins')) 
#     )]
    
#     layout = {
#         'title': {
#             'text': 'Crime rate per 100K people in the world',
#             'font': {
#                 'family': 'Poppins'
#             }
#         },
#         'geo': {
#             'showframe': False,
#             'projection_type': 'equirectangular'
#         },
#         'margin': {'l': 0, 'r': 50, 't': 50, 'b': 0}
#     }
    
#     filtered_df_lowest = df[df['Year'] == year].nsmallest(5, 'Criminality Rate')
#     fig_lowest = go.Figure(go.Bar(
#         y=filtered_df_lowest['Criminality Rate'],
#         x=filtered_df_lowest['Country Code'],
#         text=filtered_df_lowest['Criminality Rate'].round(2),
#         hovertext=filtered_df_lowest['Country'],
#         textposition='outside',
#         orientation='v',
#         width=0.5,
#         marker=dict(color='#FEDA78'),
#         hoverlabel=dict(font=dict(family='Poppins'))
#     ))
#     fig_lowest.update_layout(
#         margin=dict(l=50, r=50, t=50, b=50),
#         title=dict(text=f"Top 5 countries with the lowest crime rate in {year}", font=dict(family='Poppins')),
#         xaxis_title="Country",
#         yaxis_title="Crime rate",
#         xaxis_title_font=dict(size=11, family='Poppins'),
#         yaxis_title_font=dict(size=11, family='Poppins'),
#         bargap=0.1,  
#         plot_bgcolor='rgba(255, 255, 255, 0.9)',
#         paper_bgcolor='rgba(255, 255, 255, 0.9)',
#         yaxis=dict(gridcolor='rgb(220, 220, 220)'),  
#         title_font=dict(size=15),
#         yaxis_range=[0, filtered_df_lowest['Criminality Rate'].max() * 1.1]
#     )
    
#     filtered_df_highest = df[df['Year'] == year].nlargest(5, 'Criminality Rate')
#     fig_highest = go.Figure(go.Bar(
#         y=filtered_df_highest['Criminality Rate'],
#         x=filtered_df_highest['Country Code'],
#         text=filtered_df_highest['Criminality Rate'].round(2),
#         hovertext=filtered_df_highest['Country'],
#         textposition='outside',
#         orientation='v',
#         width=0.5,
#         marker=dict(color='#880026'),
#         hoverlabel=dict(font=dict(family='Poppins'))
#     ))
#     fig_highest.update_layout(
#         margin=dict(l=50, r=50, t=50, b=50),
#         title=dict(text=f"Top 5 countries with the highest crime rate in {year}", font=dict(family='Poppins')),
#         xaxis=dict(title='Country', tickfont=dict(family='Poppins')),
#         yaxis=dict(title="Crime rate", tickfont=dict(family='Poppins'), gridcolor='rgb(220, 220, 220)'),
#         xaxis_title_font=dict(size=11, family='Poppins'),
#         yaxis_title_font=dict(size=11, family='Poppins'), 
#         bargap=0.1, 
#         plot_bgcolor='rgba(255, 255, 255, 0.9)',
#         paper_bgcolor='rgba(255, 255, 255, 0.9)', 
#         title_font=dict(size=15),
#         yaxis_range=[0, filtered_df_highest['Criminality Rate'].max() * 1.1]
#     )
    
#     return {'data': data, 'layout': layout}, fig_lowest, fig_highest

# @callback(
#     Output('url', 'href'),
#     Output('url', 'refresh'),
#     [Input('crime-map', 'clickData')] 
# )
# def update_url_on_click(click_data):
#     if click_data is not None:
#         selected_country = click_data['points'][0]['location']
#         return f'/grafic?country={selected_country}', True

#     return '/map', False