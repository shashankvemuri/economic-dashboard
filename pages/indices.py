# Import Dependencies
import dash
from dash import Dash, dcc, Output, Input, dash_table, html, callback
import dash_bootstrap_components as dbc
import pandas_datareader.data as pdr
import plotly.express as px
import yfinance as yf
import pandas as pd
import datetime
yf.pdr_override()

dash.register_page(__name__, path='/indices', name='Stock Market Indices') # '/' is home page

# Dates
start = datetime.datetime.today() - datetime.timedelta(days=365*5)
end = datetime.datetime.today()
today = str(end.date())

indices_graph = dcc.Graph(id="indices-time-series-chart")
indices_dropdown = dcc.Dropdown(
        id="ticker",
        options=["S&P 500", "NASDAQ", "Dow 30", "Russell 2000"],
        value="S&P 500",
        clearable=False,
    )

# App Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("Stock Market Indices", style={"text-align": "center", "padding": "50px"})
        ])
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            dbc.Col(indices_dropdown, width=12)], align="center"
        ),
            dbc.Col(indices_graph, width=8),
    ]),
], fluid=True)

# Interactivity
@callback(
    Output("indices-time-series-chart", "figure"), 
    Input("ticker", "value"))
def update_graphs(ticker):
    if ticker == "S&P 500":
        indices_df = pdr.get_data_yahoo("^GSPC", start, end)

    elif ticker == "NASDAQ":
        indices_df = pdr.get_data_yahoo("^IXIC", start, end)

    elif ticker == "Dow 30":
        indices_df = pdr.get_data_yahoo("^DJI", start, end)

    elif ticker == "Russell 2000":
        indices_df = pdr.get_data_yahoo("^RUT", start, end)
    
    indices_fig = px.line(indices_df, x=indices_df.index, y=indices_df["Adj Close"], title=f"{ticker} Chart", labels={"Adj Close": f"{ticker} Close"}).update_layout(title_x=0.5)
    return indices_fig