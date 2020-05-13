import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go
import pandas as pd
import numpy as np

df = pd.read_csv("https://raw.githubusercontent.com/ajordan226/DataVisual/master/sneakerdata.csv")
df2 = pd.read_csv("https://raw.githubusercontent.com/ajordan226/DataVisual/master/states.csv")

def selected_points(clickData):
    selected_index = []
    selected_index.append(df2[df2['name'] == clickData].index.values.astype(int)[0])
    return selected_index

def generate_line_graph(dates, sale_price, shoe):
    new_trace = go.Scatter(x = dates, y = sale_price,
                    mode = 'markers+lines',
                    name = shoe,
                    marker = dict(
                        color = 'slateblue',
                        size = 7,
                        line = dict(
                            colorscale = 'mint'
                        )
                    ))

    layout = go.Layout(
        title = 'Time Series of the ' + str(shoe),
        xaxis_title = 'Dates',
        yaxis_title = 'Sale Prices (USD)',
        xaxis = dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider = dict(
                visible = True
            )
        )
    )
    return {"data" : [new_trace], "layout" : layout}

def generate_map(averages):
    df2['text'] = df2['name']
    
    initials = [i for i in df2['state']]
    
    data = go.Choropleth(
        locations = initials,
        z = averages,
        locationmode = 'USA-states',
        customdata = df2['name'],
        colorscale = 'tempo',
        colorbar_title = "USD",
        text = df2['text'],
        
    )

    return {'data' : [data],
            'layout' : go.Layout( title_text = '2017-2019 Mean Prices by State',
            geo_scope = 'usa', clickmode = 'event+select')}

def generate_bubble_plot(average_retail, average_sale, total_sales):
    states = df['Buyer Region'].unique().tolist()
    
    hover_text = []
    for i in range(51):
        hover_text.append(('Buyer Region: {state}<br>'+
                                'Sale Price: {salePrice}<br>'+
                                'Retail Price: {retailPrice}<br>'+
                                'Total Sales: {total}<br>').format(state = states[i],
                                                        salePrice = average_sale[i],
                                                        retailPrice = average_retail[i],
                                                        total = total_sales[i]))

    data = go.Scatter(
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
            ),
        )

    layout = go.Layout(
        title = 'Customer Willingness to Buy',
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

    return {'data' : [data], 'layout' : layout}

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
                    html.P('Choose Brand: '),
                    dcc.Dropdown(
                        id = 'Shoe Brands',
                        options=[
                            {'label': 'Off-White', 'value': 'Off-White'},
                            {'label': 'Yeezy', 'value': 'Yeezy'},
                        ],
                        style = {'width' : '70%'},
                        value = 'Off-White',
                        clearable = False
                    ),
            ], className = 'six columns', style = {'margin-top' : '20', 'display' : 'inline-block'}),
            html.Div([
                    html.P('Choose Shoe: '),
                    dcc.Dropdown(
                        id = 'Shoes',
                        options=[{'label': shoe, 'value': shoe} for shoe in 
                                df.loc[(df['Brand'] == 'Off-White'), 'Sneaker Name'].unique()],
                        style = {'width' : '80%'},
                        value = df.loc[(df['Brand'] == 'Off-White'), 'Sneaker Name'].unique().tolist()[0],
                        clearable = False
                    ),
            ], className = 'six columns', style = {'margin-top' : '20', 'display' : 'inline-block'})
        ], className = 'row'),

        # Bes Line Graph - This is my part here, to do the line chart
        html.Div([
            html.Div([
                dcc.Graph(
                    id = 'lineChart'
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
    states = df['Buyer Region'].unique().tolist()

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


    return generate_bubble_plot(average_retail, average_sale, total_sales)

@app.callback(
    Output('map', 'figure'),
    [Input('Brands', 'value'),
    Input('scatterplot', 'clickData')])
def update_map(selector, scatterplot_click_data):
    states = [i for i in df2['name']]
    
    if selector == 'B':
        averages = []
        for i in states:
            b = df.loc[(df['Buyer Region'] == i), 'Sale Price'].mean()
            averages.append(b)
    elif selector == 'OFW':
        averages = []
        for i in states:
            ofw = df.loc[(df.Brand == 'Off-White') & (df['Buyer Region'] == i), 'Sale Price'].mean()
            averages.append(ofw)
    elif selector == 'YZY':
        averages = []
        for i in states:
            yzy = df.loc[(df.Brand == ' Yeezy') & (df['Buyer Region'] == i), 'Sale Price'].mean()
            averages.append(yzy)

    return generate_map(averages)

@app.callback(
    Output('Shoes', 'options'),
    [Input('Shoe Brands', 'value')]
)
def update_date_dropdown(selector):
    if selector == 'Yeezy':
        return [{'label': shoe, 'value': shoe} for shoe in 
                df.loc[(df['Brand'] == ' Yeezy'), 'Sneaker Name'].unique()]
    else:
        return [{'label': shoe, 'value': shoe} for shoe in 
                df.loc[(df['Brand'] == 'Off-White'), 'Sneaker Name'].unique()]

@app.callback(
    Output('lineChart', 'figure'),
    [Input('Shoes', 'value')])
def update_line(selector):
    new_df = pd.read_csv("https://raw.githubusercontent.com/ajordan226/DataVisual/master/sneakerdata.csv")
    
    shoes = new_df['Sneaker Name'].unique().tolist()
    for shoe in shoes:
        if selector == shoe:
            new_df = new_df.groupby(["Order Date", "Sneaker Name"]).mean().reset_index()
            sale_prices = new_df.loc[new_df["Sneaker Name"] == shoe, 'Sale Price']
            new_df['Order Date'] = pd.to_datetime(new_df['Order Date'])
            dates = pd.DatetimeIndex(new_df['Order Date'].unique()).tolist()
            dates.sort(reverse = True)
            shoe_name = shoe
    return generate_line_graph(dates, sale_prices, shoe_name)




if __name__ == '__main__':
    app.run_server(debug=True)
