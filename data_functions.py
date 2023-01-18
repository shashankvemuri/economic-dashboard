# Import Dependencies
import pandas_datareader.data as pdr
import yfinance as yf
import pandas as pd
import datetime
yf.pdr_override()

# Dates
start = datetime.datetime.today() - datetime.timedelta(days=365*5)
end = datetime.datetime.today()
today = str(end.date())

# Treasury rates
def get_treasury_rates():
    url = f'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{str(end)[:4]}/all?type=daily_treasury_yield_curve&field_tdr_date_value={str(end)[:4]}&page&_format=csv'
    rates_df = pd.read_csv(url)
    return rates_df

# Unemployment values
def get_unemployment_data():
    url = 'https://data.bls.gov/timeseries/LNS14000000'
    unemp_df = pd.read_html(url)[1]
    unemp_df = pd.melt(unemp_df, id_vars=['Year'], var_name=['Month'])
    unemp_df['Date'] = pd.to_datetime(unemp_df['Year'].astype(str) + '-' + unemp_df['Month'].astype(str))
    unemp_df = unemp_df.sort_values(by=['Date']).drop(columns=['Month', 'Year']).reset_index(drop=['index']).set_index('Date')
    unemp_df.columns = ['Unemployment %']
    return unemp_df

# Inflation data
def get_inflation_data():
    url = 'https://www.usinflationcalculator.com/inflation/historical-inflation-rates/'
    inflation_df = pd.read_html(url)[0].drop(columns=["Ave"]).tail(10)
    inflation_df = pd.melt(inflation_df, id_vars=['Year'], var_name=['Month'])
    inflation_df['Date'] = pd.to_datetime(inflation_df['Year'].astype(str) + '-' + inflation_df['Month'].astype(str))
    inflation_df = inflation_df.sort_values(by=['Date']).drop(columns=['Month', 'Year']).reset_index(drop=['index']).set_index('Date')
    inflation_df.columns = ['Inflation %']
    return inflation_df

# GDP
def get_gdp_data():
    url = 'https://www.multpl.com/us-gdp-inflation-adjusted/table/by-year'
    gdp_df = pd.read_html(url)[0].set_index('Date').head(10)
    gdp_df.columns = ['GDP']
    gdp_df['GDP'] = gdp_df['GDP'].str.strip()
    gdp_df['GDP'] = gdp_df['GDP'].str.extract('(\d+\D\d+)')
    gdp_df['GDP'] = gdp_df['GDP'].apply(float)
    gdp_df.index = pd.to_datetime(gdp_df.index)
    return gdp_df

# Mortgage Rates
def get_mortgage_rates():
    storage_options = {'User-Agent': 'Mozilla/5.0'}
    mortgage_df = pd.read_excel("https://www.freddiemac.com/pmms/docs/historicalweeklydata.xlsx", storage_options=storage_options)
    mortgage_df.columns = ['Date', '30yr FRM', '30yr fees', '15yr FRM', '15yr fees', '5/1 ARM', '5/1 ARM fees', '5/1 ARM margin', '30yr FRM/ 5/1 ARM Spread']
    mortgage_df = mortgage_df.set_index('Date').drop(columns=['30yr fees', '15yr fees', '5/1 ARM', '5/1 ARM fees', '5/1 ARM margin', '30yr FRM/ 5/1 ARM Spread'])[:-1].tail(100)
    return mortgage_df

# VIX
def get_vix_data():
    vix_df = pdr.get_data_yahoo("^VIX", start, end)
    return vix_df

# NAAIM
def get_naaim_data():
        try:
            today = datetime.date.today()
            offset = (today.weekday() - 2) % 7
            naaim_date = str(today - datetime.timedelta(days=offset))
            naaim_df = pd.read_excel(f"https://www.naaim.org/wp-content/uploads/{naaim_date[:4]}/{naaim_date[5:7]}/USE_Data-since-Inception_{naaim_date}.xlsx", index_col=0).iloc[::-1].tail(104)
        except:
            today = datetime.date.today()
            offset = (today.weekday() - 2) % 7
            naaim_date = str(today - datetime.timedelta(days=(offset+7)))
            naaim_df = pd.read_excel(f"https://www.naaim.org/wp-content/uploads/{naaim_date[:4]}/{naaim_date[5:7]}/USE_Data-since-Inception_{naaim_date}.xlsx", index_col=0).iloc[::-1].tail(104)

        return naaim_df

# US Personal Savings Rate
def get_savings_rates():
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PSAVERT&scale=left&cosd=1959-01-01&coed=2022-11-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={today}&revision_date={today}&nd=1959-01-01"
    savings_df = pd.read_csv(url, index_col=0).tail(100)
    return savings_df

# M2 Money Supply
def get_m2_supply():
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=M2SL&scale=left&cosd=1959-01-01&coed=2022-11-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={today}&revision_date={today}&nd=1959-01-01"
    m2_df = pd.read_csv(url, index_col=0).tail(100)
    return m2_df