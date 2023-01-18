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

dash.register_page(__name__, path='/', name='Macro Indicators') # '/' is home page

# Dates
start = datetime.datetime.today() - datetime.timedelta(days=365*5)
end = datetime.datetime.today()
today = str(end.date())

# Data
rates_df = dfn.get_treasury_rates()
unemp_df = dfn.get_unemployment_data()
inflation_df = dfn.get_inflation_data()
gdp_df = dfn.get_gdp_data()
mortgage_df = dfn.get_mortgage_rates()
savings_df = dfn.get_savings_rates()
m2_df = dfn.get_m2_supply()

#Plots
unemp_fig = px.line(unemp_df, title="Unemployment %", labels={"value": "Unemployment %","index": "Date"}).update_layout(title_x=0.5, showlegend=False)
inflation_fig = px.line(inflation_df, title="Inflation %", labels={"value" : "CPI Print"}).update_layout(title_x=0.5, showlegend=False)
savings_fig = px.line(savings_df, x=savings_df.index, y=savings_df["PSAVERT"], title="Personal Savings Rate", labels={"PSAVERT" : "Savings %", "DATE": "Date"}).update_layout(title_x=0.5)
m2_fig = px.line(m2_df, title="M2 Money Supply", labels={"value" : "Billions of Dollars", "DATE": "Date"}).update_layout(title_x=0.5, showlegend=False)
gdp_fig = px.line(gdp_df, x=gdp_df.index, y=gdp_df["GDP"], title="Gross Domestic Product", labels={"GDP" : "GDP (trillions)", "index": "Date"}).update_layout(title_x=0.5)
mortgage_fig = px.line(mortgage_df, x=mortgage_df.index, y=[mortgage_df["30yr FRM"], mortgage_df["15yr FRM"]], title="Mortgage Rate %", labels={"value" : "Rate %"}).update_layout(title_x=0.5)

treasury_rates = dash_table.DataTable(rates_df.to_dict('records'), [{"name": i, "id": i} for i in rates_df.columns])
unemp_graph = dcc.Graph(id="unemp-time-series-chart", figure=unemp_fig)
inflation_graph = dcc.Graph(id="inflation-time-series-chart", figure=inflation_fig)
savings_graph = dcc.Graph(id="savings-time-series-chart", figure=savings_fig)
m2_graph = dcc.Graph(id="m2-time-series-chart", figure=m2_fig)
gdp_graph = dcc.Graph(id="gdp-time-series-chart", figure=gdp_fig)
mortgage_graph = dcc.Graph(id="mortgage-time-series-chart", figure=mortgage_fig)

# App Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("Macroeconomic Indicators", style={"text-align": "center", "padding": "50px"})
        ])
    ], justify='center'),
    dbc.Row([
        dbc.Col(unemp_graph),
        dbc.Col(inflation_graph),
        dbc.Col(savings_graph),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(m2_graph, style={"padding-top": "10px"})
            ]),
        dbc.Col([
            html.Div(gdp_graph, style={"padding-top": "10px"})
            ]),
        dbc.Col([
            html.Div(mortgage_graph, style={"padding-top": "10px"})
            ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.H4("Treasury Rates", style={"text-align": "center", "padding": "50px"})
        ])
    ], justify='center'),
    dbc.Row([
        dbc.Col(
            html.Div([treasury_rates], style={"padding-bottom": "50px"})
            , width=10)
    ], justify='center')
], fluid=True)