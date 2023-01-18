# Import Dependencies
import dash
from dash import Dash, dcc, Output, Input, dash_table, html, callback
import dash_bootstrap_components as dbc
import pandas_datareader.data as pdr
import plotly.express as px
import yfinance as yf
import pandas as pd
import datetime
import data_functions as dfn
yf.pdr_override()

dash.register_page(__name__, path='/sentiment', name='Market Sentiment') # '/' is home page

# Dates
start = datetime.datetime.today() - datetime.timedelta(days=365*5)
end = datetime.datetime.today()
today = str(end.date())

# Data
vix_df = dfn.get_vix_data()
naaim_df = dfn.get_naaim_data()

# Figures
vix_fig = px.line(vix_df, x=vix_df.index, y=vix_df["Adj Close"], title=f"VIX Chart", labels={"Adj Close": f"VIX Close"}).update_layout(title_x=0.5)
naaim_fig = px.line(naaim_df, x=naaim_df.index, y=naaim_df["NAAIM Number"], title="NAAIM Exposure Index").update_layout(title_x=0.5)

vix_graph = dcc.Graph(id="vix-time-series-chart", figure=vix_fig)
naaim_graph = dcc.Graph(id="naaim-time-series-chart", figure=naaim_fig)

# App Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("Sentiment", style={"text-align": "center", "padding": "50px"})
        ])
    ], justify='center'),
    dbc.Row([
        dbc.Col(vix_graph),
        dbc.Col(naaim_graph),
    ]),
], fluid=True)