# Import Dependencies
from dash import Dash, dcc, Output, Input, dash_table, html
import dash_bootstrap_components as dbc
import pandas_datareader.data as pdr
import plotly.express as px
import yfinance as yf
import pandas as pd
import datetime
yf.pdr_override()

# Dates
start = datetime.datetime.today() - datetime.timedelta(days=365*5)
end = datetime.datetime.today()
today = str(end.date())

# Treasury rates
rates_df = pd.read_csv(f'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{str(end)[:4]}/all?type=daily_treasury_yield_curve&field_tdr_date_value={str(end)[:4]}&page&_format=csv')

# Unemployment values
url = 'https://data.bls.gov/timeseries/LNS14000000'
unemp_df = pd.read_html(url)[1]
unemp_df = pd.melt(unemp_df, id_vars=['Year'], var_name=['Month'])
unemp_df['Date'] = pd.to_datetime(unemp_df['Year'].astype(str) + '-' + unemp_df['Month'].astype(str))
unemp_df = unemp_df.sort_values(by=['Date']).drop(columns=['Month', 'Year']).reset_index(drop=['index']).set_index('Date')
unemp_df.columns = ['Unemployment %']

# Inflation data
url = 'https://www.usinflationcalculator.com/inflation/historical-inflation-rates/'
inflation_df = pd.read_html(url)[0].drop(columns=["Ave"]).tail(10)
inflation_df = pd.melt(inflation_df, id_vars=['Year'], var_name=['Month'])
inflation_df['Date'] = pd.to_datetime(inflation_df['Year'].astype(str) + '-' + inflation_df['Month'].astype(str))
inflation_df = inflation_df.sort_values(by=['Date']).drop(columns=['Month', 'Year']).reset_index(drop=['index']).set_index('Date')
inflation_df.columns = ['Inflation %']

# GDP
url = 'https://www.multpl.com/us-gdp-inflation-adjusted/table/by-year'
gdp_df = pd.read_html(url)[0].set_index('Date').head(10)
gdp_df.columns = ['GDP']
gdp_df['GDP'] = gdp_df['GDP'].str.strip()
gdp_df['GDP'] = gdp_df['GDP'].str.extract('(\d+\D\d+)')
gdp_df['GDP'] = gdp_df['GDP'].apply(float)
gdp_df.index = pd.to_datetime(gdp_df.index)

# Mortgage Rates
storage_options = {'User-Agent': 'Mozilla/5.0'}
mortgage_df = pd.read_excel("https://www.freddiemac.com/pmms/docs/historicalweeklydata.xlsx", storage_options=storage_options)
mortgage_df.columns = ['Date', '30yr FRM', '30yr fees', '15yr FRM', '15yr fees', '5/1 ARM', '5/1 ARM fees', '5/1 ARM margin', '30yr FRM/ 5/1 ARM Spread']
mortgage_df = mortgage_df.set_index('Date').drop(columns=['30yr fees', '15yr fees', '5/1 ARM', '5/1 ARM fees', '5/1 ARM margin', '30yr FRM/ 5/1 ARM Spread'])[:-1].tail(100)

# VIX
vix_df = pdr.get_data_yahoo("^VIX", start, end)

# NAAIM
today = datetime.date.today()
offset = (today.weekday() - 2) % 7
naaim_date = str(today - datetime.timedelta(days=offset))
naaim_df = pd.read_excel(f"https://www.naaim.org/wp-content/uploads/{naaim_date[:4]}/{naaim_date[5:7]}/USE_Data-since-Inception_{naaim_date}.xlsx", index_col=0).iloc[::-1].tail(104)

# US Personal Savings Rate
savings_df = pd.read_csv(f"https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PSAVERT&scale=left&cosd=1959-01-01&coed=2022-11-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={today}&revision_date={today}&nd=1959-01-01", index_col=0).tail(100)

# M2 Money Supply
m2_df = pd.read_csv(f"https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=M2SL&scale=left&cosd=1959-01-01&coed=2022-11-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={today}&revision_date={today}&nd=1959-01-01", index_col=0).tail(100)

## Create Dash App
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

indices_graph = dcc.Graph(id="indices-time-series-chart")
indices_dropdown = dcc.Dropdown(
        id="ticker",
        options=["S&P 500", "NASDAQ", "Dow 30", "Russell 2000"],
        value="S&P 500",
        clearable=False,
    )
treasury_rates = dash_table.DataTable(rates_df.to_dict('records'), [{"name": i, "id": i} for i in rates_df.columns])
vix_graph = dcc.Graph(id="vix-time-series-chart",)
naaim_graph = dcc.Graph(id="naaim-time-series-chart")
unemp_graph = dcc.Graph(id="unemp-time-series-chart")
inflation_graph = dcc.Graph(id="inflation-time-series-chart")
savings_graph = dcc.Graph(id="savings-time-series-chart")
m2_graph = dcc.Graph(id="m2-time-series-chart")
gdp_graph = dcc.Graph(id="gdp-time-series-chart")
mortgage_graph = dcc.Graph(id="mortgage-time-series-chart")

# App Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Economic Dashboard", style={"text-align": "center", "padding": "50px"})
        ])
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            html.H4("Stock Market Indices", style={"text-align": "center"}),
            dbc.Col(indices_dropdown, width=12)], align="center"
        ),
            dbc.Col(indices_graph, width=8),
    ]),
    dbc.Row([
        dbc.Col([
            html.H4("Sentiment", style={"text-align": "center", "padding": "50px"})
        ])
    ], justify='center'),
    dbc.Row([
        dbc.Col(vix_graph),
        dbc.Col(naaim_graph),
    ]),
    dbc.Row([
        dbc.Col([
            html.H4("Macro Indicators", style={"text-align": "center", "padding": "50px"})
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

# Interactivity
@app.callback(
    Output("indices-time-series-chart", "figure"), 
    Output("vix-time-series-chart", "figure"), 
    Output("naaim-time-series-chart", "figure"), 
    Output("unemp-time-series-chart", "figure"), 
    Output("inflation-time-series-chart", "figure"), 
    Output("savings-time-series-chart", "figure"), 
    Output("m2-time-series-chart", "figure"), 
    Output("gdp-time-series-chart", "figure"), 
    Output("mortgage-time-series-chart", "figure"), 
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
    vix_fig = px.line(vix_df, x=vix_df.index, y=vix_df["Adj Close"], title=f"VIX Chart", labels={"Adj Close": f"{ticker} Close"}).update_layout(title_x=0.5)
    naaim_fig = px.line(naaim_df, x=naaim_df.index, y=naaim_df["NAAIM Number"], title="NAAIM Exposure Index").update_layout(title_x=0.5)
    unemp_fig = px.line(unemp_df, title="Unemployment %", labels={"value": "Unemployment %","index": "Date"}).update_layout(title_x=0.5, showlegend=False)
    inflation_fig = px.line(inflation_df, title="Inflation %", labels={"value" : "CPI Print"}).update_layout(title_x=0.5, showlegend=False)
    savings_fig = px.line(savings_df, x=savings_df.index, y=savings_df["PSAVERT"], title="Personal Savings Rate", labels={"PSAVERT" : "Savings %", "DATE": "Date"}).update_layout(title_x=0.5)
    m2_fig = px.line(m2_df, title="M2 Money Supply", labels={"value" : "Billions of Dollars", "DATE": "Date"}).update_layout(title_x=0.5, showlegend=False)
    gdp_fig = px.line(gdp_df, x=gdp_df.index, y=gdp_df["GDP"], title="Gross Domestic Product", labels={"GDP" : "GDP (trillions)", "index": "Date"}).update_layout(title_x=0.5)
    mortgage_fig = px.line(mortgage_df, x=mortgage_df.index, y=[mortgage_df["30yr FRM"], mortgage_df["15yr FRM"]], title="Mortgage Rate %", labels={"value" : "Rate %"}).update_layout(title_x=0.5)
    return indices_fig, vix_fig, naaim_fig, unemp_fig, inflation_fig, savings_fig, m2_fig, gdp_fig, mortgage_fig

# Run app
if __name__=='__main__':
    app.run_server(debug=True)