import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go
import pandas as pd
import numpy as np

df = pd.read_csv("C:\\Users\\ajord\\DataVisual\\sneakerdata.csv")

shoes = df['Sneaker Name'].unique()
fig2 = go.Figure()

for shoe in shoes:
    fig2.add_trace(go.Scatter(x = df['Order Date'], y = df['Sale Price'],
                    mode = 'lines',
                    name = shoe))

fig2.update_layout(title = 'Sale Prices of Shoes Over Time',
                   xaxis_title = 'Date',
                   yaxis_title = 'Sale Price (USD)')

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
                    id = 'map'
                    )
            ], className = 'twelve columns'),
        ], className = 'row'),

        html.Div([ 
            html.Div([    
                    dcc.Graph(
                        id = 'scatterplot'
                    )
            ], className = 'twelve columns')
        ], className = 'row'),

        html.Div([
            html.Div([
                dcc.Graph(
                    id = 'line chart',
                    figure = fig2
                    )
            ], className = 'twelve columns'),
        ], className = 'row')
], className = 'ten columns offset-by-one' )
)

@app.callback(
    Output('scatterplot', 'figure'),
    [Input('Brands', 'value'),
    Input('map', 'clickData')])
def update_scatter(selector, map_click_data):
    df2 = pd.read_csv("C:\\Users\\ajord\\DataVisual\\sneakerdata.csv")
    
    states = df2['Buyer Region'].unique().tolist()

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

    fig = go.Scatter(
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
            showscale = True,
            )
    )

    layout = dict(
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
        clickmode = 'event+select'
    )

    return {'data' : [fig], 'layout' : layout}

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

    fig3 = go.Choropleth(
        locations = initials, 
        z = averages, 
        locationmode = 'USA-states',
        customdata = df2_states['name'], 
        colorscale = 'tempo',
        colorbar_title = "USD",
        text = df2_states['text'],
        
    )

    return {'data' : [fig3],
            'layout' : go.Layout( title_text = '2017-2019 Mean Prices by State',
            geo_scope = 'usa', clickmode = 'event+select')}



        

if __name__ == '__main__':
    app.run_server(debug=True)