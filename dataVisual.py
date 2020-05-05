import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go
import pandas as pd
import numpy as np

df = pd.read_csv("C:\\Users\\ajord\\DataVisual\\sneakerdata.csv")

# Temporary Bubble Plot
fig = go.Figure(data = [go.Scatter(
    x = [1, 2, 3, 4], 
    y = [10, 11, 12, 13],
    mode = 'markers',
    marker_size = [40, 60, 80, 100])
])

# Temporary Chloropleth Map
df_states = pd.read_csv("C:\\Users\\ajord\\Documents\\states.csv")

initials = []
for i in df_states['state']:
    initials.append(i)

fig3 = go.Figure(data=go.Choropleth(
    locations = initials, 
    z = df['Sale Price'], 
    locationmode = 'USA-states', 
    colorscale = 'tempo',
))

fig3.update_layout(
    title_text = '2017-2019 Mean Prices by State',
    geo_scope = 'usa', 
)


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
                    figure = fig3,
                    id = 'map'
                    )
            ], className = 'twelve columns'),
        ], className = 'row'),

        html.Div([ 
            html.Div([    
                    dcc.Graph(
                        figure = fig,
                        id = 'scatterplot'
                    )
            ], className = 'twelve columns')
        ], className = 'row')
], className = 'ten columns offset-by-one' )
)

@app.callback(
    Output('scatterplot', 'figure'),
    [Input('Brands', 'value')])
def update_scatter(selector):
    df2 = pd.read_csv("C:\\Users\\ajord\\DataVisual\\sneakerdata.csv")
    
    states = []
    for i in df2['Buyer Region']:
        if i not in states:
            states.append(i)
    
    if selector == "B":
        total_sales = []
        for i in states:
            sales = df.loc[(df['Buyer Region'] == i), 'Order Date']
            total_sales.append(sales.size)

        average_sale = []
        for i in states:
            mean = df.loc[(df['Buyer Region'] == i), 'Sale Price'].mean()
            average_sale.append(mean)

        average_retail = []
        for i in states:
            mean = df.loc[(df['Buyer Region'] == i), 'Retail Price'].mean()
            average_retail.append(mean)
    elif selector == "OFW":
        total_sales = []
        for i in states:
            sales = df2.loc[(df2['Buyer Region'] == i) & (df2.Brand == 'Off-White'), 'Order Date']
            total_sales.append(sales.size)

        average_sale = []
        for i in states:
            mean = df2.loc[(df2['Buyer Region'] == i) & (df2.Brand == 'Off-White'), 'Sale Price'].mean()
            average_sale.append(mean)

        average_retail = []
        for i in states:
            mean = df2.loc[(df2['Buyer Region'] == i) & (df2.Brand == 'Off-White'), 'Retail Price'].mean()
            average_retail.append(mean)
    elif selector == "YZY":
        total_sales = []
        for i in states:
            sales = df2.loc[(df2['Buyer Region'] == i) & (df2.Brand == ' Yeezy'), 'Order Date']
            total_sales.append(sales.size)

        average_sale = []
        for i in states:
            mean = df2.loc[(df2['Buyer Region'] == i) & (df2.Brand == ' Yeezy'), 'Sale Price'].mean()
            average_sale.append(mean)

        average_retail = []
        for i in states:
            mean = df2.loc[(df2['Buyer Region'] == i) & (df2.Brand == ' Yeezy'), 'Retail Price'].mean()
            average_retail.append(mean)

    hover_text = []
    for i in range(51):
        hover_text.append(('Buyer Region: {state}<br>'+
                            'Sale Price: {salePrice}<br>'+
                            'Retail Price: {retailPrice}<br>'+
                            'Total Sales: {total}<br>').format(state = states[i],
                                                    salePrice = average_sale[i],
                                                    retailPrice = average_retail[i],
                                                    total = total_sales[i]))

    fig = go.Figure(data = [go.Scatter(
        x = average_retail,
        y = average_sale,
        mode = 'markers',
        text = hover_text,
        marker = dict(
            color = total_sales,
            colorscale = 'Agsunset',
            size = total_sales,
            colorbar_title = 'Total Sales',
            sizemode = 'area',
            sizeref = 2. * max(total_sales)/(100**2),
            showscale = True
            )
    )])

    fig.update_layout(
        title = 'Sales Per Region',
        xaxis = dict(
            title = 'Retail Price (USD)',
            gridcolor = 'white',
            type = 'log',
            gridwidth = 2,
        ),
        yaxis = dict(
            title = 'Sale Price (USD)',
            gridcolor = 'white',
            gridwidth = 2,
        ),
        paper_bgcolor = 'rgb(243, 243, 243)',
        plot_bgcolor = 'rgb(243, 243, 243)',
    )
        
    figure = fig

    return figure

@app.callback(
    Output('map', 'figure'),
    [Input('Brands', 'value')])
def update_map(selector):
    df2_states = pd.read_csv("C:\\Users\\ajord\\DataVisual\\states.csv")
    df2_states['text'] = df2_states['name']

    initials = []
    for i in df2_states['state']:
        initials.append(i)

    s = []
    for i in df2_states['name']:
        s.append(i)
    if selector == 'B':
        averages = []
        for i in s:
            b = df.loc[(df['Buyer Region'] == i), 'Sale Price'].mean()
            averages.append(b)
    elif selector == 'OFW':
        averages = []
        for i in s:
            ofw = df.loc[(df.Brand == 'Off-White') & (df['Buyer Region'] == i), 'Sale Price'].mean()
            averages.append(ofw)
    elif selector == 'YZY':
        averages = []
        for i in s:
            yzy = df.loc[(df.Brand == ' Yeezy') & (df['Buyer Region'] == i), 'Sale Price'].mean()
            averages.append(yzy)

    fig3 = go.Figure(data = go.Choropleth(
        locations = initials, 
        z = averages, 
        locationmode = 'USA-states', 
        colorscale = 'tempo',
        colorbar_title = "USD",
        text = df2_states['text'],
    ))

    fig3.update_layout(
        title_text = '2017-2019 Mean Prices by State',
        geo_scope = 'usa', 
    )

    figure = fig3
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)