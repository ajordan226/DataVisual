import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go
import pandas as pd
import numpy as np

dataframe = pd.read_csv("C:\\Users\\ajord\\Documents\\sneakerdata.csv")
df = dataframe.iloc[:1000]


fig = go.Figure(data = go.Scattergl(
    x = df['Shoe Size'],
    y = df['Sale Price'],
    mode = 'markers',
    marker = dict(
        size = 10,
        color = np.random.randn(1000),
        colorscale ='Viridis',
        line_width = 1
    ),
    
    text = df['Sneaker Name']
))

fig.update_layout(
    title = 'Shoe Size Vs Sale Price',
    xaxis = dict(
        title = 'Shoe Size (US Mens)',
        titlefont = dict(
            size = 20
        )
    ),
    yaxis = dict(
        title = 'Sale Price ($)',
        titlefont = dict(
            size = 20
        )
    )
)

states = []
for i in df['Buyer Region']:
    if i not in states:
        states.append(i)

mean_ofw = []
for i in states:
    ofw = df.loc[(df.Brand == 'Off-White') & (df['Buyer Region'] == i), 'Sale Price'].mean()
    mean_ofw.append(ofw)

mean_yzy = []
for i in states:
    yzy = df.loc[(df.Brand == ' Yeezy') & (df['Buyer Region'] == i), 'Sale Price'].mean()
    mean_yzy.append(yzy)

fig2 = go.Figure(data=[
    go.Bar(name = 'Off-White', x = states, y = mean_ofw ),
    go.Bar(name = 'Yeezy', x = states, y = mean_yzy)
])

fig2.update_layout(
    title = 'Mean Prices per State',
    barmode = 'group',
    xaxis = dict(
        title = 'States',
        titlefont = dict(
            size = 20
        )
    ),
    yaxis = dict(
        title = 'Average Sale Price($)',
        titlefont = dict(
            size = 20
        )
    )
)

df_states = pd.read_csv("C:\\Users\\ajord\\Documents\\states.csv")
df_states['text'] = df_states['name']

initials = []
for i in df_states['state']:
    initials.append(i)

s = []
for i in df_states['name']:
    s.append(i)

average_ofw = []
for i in s:
    ofw = df.loc[(df.Brand == 'Off-White') & (df['Buyer Region'] == i), 'Sale Price'].mean()
    average_ofw.append(ofw)

average_yzy = []
for i in s:
    yzy = df.loc[(df.Brand == ' Yeezy') & (df['Buyer Region'] == i), 'Sale Price'].mean()
    average_yzy.append(yzy)

fig3 = go.Figure(data=go.Choropleth(
    locations = initials, 
    z = average_ofw, 
    locationmode = 'USA-states', 
    colorscale = 'Greens',
    colorbar_title = "USD",
    text = df_states['text'],
))

fig3.update_layout(
    title_text = '2017-2019 Mean Prices for Off-White by State',
    geo_scope = 'usa', 
)

fig4 = go.Figure(data=go.Choropleth(
    locations = initials, 
    z = average_yzy, 
    locationmode = 'USA-states', 
    colorscale = 'Purples',
    colorbar_title = "USD",
    text = df_states['text'],
))

fig4.update_layout(
    title_text = '2017-2019 Mean Prices for Yeezy by State',
    geo_scope = 'usa', 
)

fig5 = go.Figure()
date = []
for i in df['Order Date']:
    if i not in date:
        date.append(i)

fig5.add_trace(go.Scatter(x = date, y = df.loc[(df['Sneaker Name'] == 'Adidas-Yeezy-Boost-350-Low-V2-Beluga'), 'Sale Price'],
                    name='Adidas-Yeezy-Boost-350-Low-V2-Beluga'))
fig5.add_trace(go.Scatter(x = date, y = df.loc[(df['Sneaker Name'] == 'Adidas-Yeezy-Boost-350-V2-Core-Black-Copper'), 'Sale Price'],
                    name='Adidas-Yeezy-Boost-350-V2-Core-Black-Copper'))
fig5.add_trace(go.Scatter(x = date, y = df.loc[(df['Sneaker Name'] == 'Adidas-Yeezy-Boost-350-V2-Core-Black-Green'), 'Sale Price'],
                     name='Adidas-Yeezy-Boost-350-V2-Core-Black-Green'))
fig5.add_trace(go.Scatter(x = date, y = df.loc[(df['Sneaker Name'] == 'Adidas-Yeezy-Boost-350-V2-Core-Black-Red'), 'Sale Price'],
                    name='Adidas-Yeezy-Boost-350-V2-Core-Black-Red'))
fig5.add_trace(go.Scatter(x = date, y = df.loc[(df['Sneaker Name'] == 'Adidas-Yeezy-Boost-350-V2-Core-Black-Red-2017'), 'Sale Price'],
                    name='Adidas-Yeezy-Boost-350-V2-Core-Black-Red-2017'))
fig5.add_trace(go.Scatter(x = date, y = df.loc[(df['Sneaker Name'] == 'Adidas-Yeezy-Boost-350-V2-Core-Black-White'), 'Sale Price'],
                     name='Adidas-Yeezy-Boost-350-V2-Core-Black-White'))
fig5.update_traces(hoverinfo ='text+name', mode = 'lines+markers')


external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    html.Div([
        html.Div([
            html.H1(children='StockX Sneaker Data',
                    className = 'nine columns'),

            html.Img(
                src = 'https://i.pinimg.com/originals/f9/80/88/f980882cfc01854b50fb460fd357af9a.jpg',
                className = 'three columns',
                style = {
                    'height' : '20%',
                    'width' : '20%',
                    'float' : 'right',
                    'position' : 'relative',
                    'margin-right': 20,
                    'margin-top' : 20
            

                },
            ),

            html.Div(children='''
                Three years of sneaker data provided by StockX,
                an online marketplace for shoes and apparel.
                ''',
                className = 'nine columns')
        ], className = 'row'),

        html.Div([
            html.Div([
                    html.P('Choose Brand: '),
                    dcc.Dropdown(
                        id = 'Brands',
                        options=[
                            {'label': 'Both', 'value': 'B'},
                            {'label': 'Off-White', 'value': 'OFW'},
                            {'label': 'Yeezy', 'value': 'YZY'},
                        ],
                        style = {'width' : '40%'},
                        value = 'B',
                        clearable = False
                    ),  
            ], className = 'twelve columns', style = {'margin-top' : '10'}),
        ], className = 'row'),
        
        html.Div([
            html.Div([
                dcc.Graph(
                    figure = fig,
                    id = 'scatterplot'
                    )
            ], className = 'twelve columns'),
        ], className = 'row'),
        
        html.Div([
            html.Div([
                dcc.Graph(
                    figure = fig5,
                    id = 'line chart'
                    )
            ], className = 'twelve columns'),
        ], className = 'row'),

    
    html.Div([ 
        html.Div([    
                dcc.Graph(
                    figure =fig3,
                    id = 'off-white map'
                )
        ], className = 'six columns'),
        html.Div([    
                dcc.Graph(
                    figure =fig4,
                    id = 'yeezy map'
                )
        ], className = 'six columns')
    ], className = 'row')
], className = 'ten columns offset-by-one' )
)

@app.callback(
    Output('scatterplot', 'figure'),
    [Input('Brands', 'value')])
def update_figure(selector):
    new_df = pd.DataFrame()
    df = dataframe.iloc[:1000]
    if selector == "B":
        df = dataframe.iloc[:1000]
    elif selector == "OFW":
        new_df = df.loc[df['Brand'] == 'Off-White']
        df = new_df
    elif selector == "YZY":
        new_df = df.loc[df['Brand'] == ' Yeezy']
        df = new_df

    fig = go.Figure(data = go.Scattergl(
    x = df['Shoe Size'],
    y = df['Sale Price'],
    mode = 'markers',
    marker = dict(
        size = 10,
        color = np.random.randn(1000),
        colorscale ='Viridis',
        line_width = 1
    ),
    
    text = df['Sneaker Name']
))

    fig.update_layout(
        title = 'Shoe Size Vs Sale Price',
        xaxis = dict(
            title = 'Shoe Size (US Mens)',
            titlefont = dict(
                size = 20
            )
        ),
        yaxis = dict(
            title = 'Sale Price ($)',
            titlefont = dict(
                size = 20
            )
        )
    )
    
    figure = fig

    return figure

'''@app.callback(
    Output('Bar', 'figure'),
    [Input('Brands', 'value')])
def update_bar_chart(selector):
    if selector == "B":
        fig2 = go.Figure(data=[
            go.Bar(name = 'Off-White', x = states, y = mean_ofw, marker_color = 'forestgreen' ),
            go.Bar(name = 'Yeezy', x = states, y = mean_yzy, marker_color = 'mediumpurple')
        ])
        fig2.update_layout(
            title = 'Mean Prices per State',
            barmode = 'group',
            xaxis = dict(
                title = 'States',
                titlefont = dict(
                    size = 20
                )
            ),
            yaxis = dict(
                title = 'Average Sale Price($)',
                titlefont = dict(
                    size = 20
                )
            )
        )
    elif selector == "OFW":
        fig2 = go.Figure(data=[
            go.Bar(name = 'Off-White', x = states, y = mean_ofw, marker_color = 'forestgreen' )
        ])
        fig2.update_layout(
            title = 'Mean Prices per State',
            xaxis = dict(
                title = 'States',
                titlefont = dict(
                    size = 20
                )
            ),
            yaxis = dict(
                title = 'Average Sale Price($)',
                titlefont = dict(
                    size = 20
                )
            )
        )
    elif selector == "YZY":
        fig2 = go.Figure(data=[
            go.Bar(name = 'Yeezy', x = states, y = mean_yzy, marker_color = 'mediumpurple')
        ])
        fig2.update_layout(
            title = 'Mean Prices per State',
            xaxis = dict(
                title = 'States',
                titlefont = dict(
                    size = 20
                )
            ),
            yaxis = dict(
                title = 'Average Sale Price($)',
                titlefont = dict(
                    size = 20
                )
            )
        )
    
    figure = fig2

    return figure'''

if __name__ == '__main__':
    app.run_server(debug=True)