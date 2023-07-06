import pandas as pd
import os 
from dotenv import load_dotenv, find_dotenv
import requests
import traceback


env_path = find_dotenv()
load_dotenv(env_path)
api_key = os.environ.get('API_KEY')

# Run once to get the csv file, later on we can just read the csv file
# For more advanced usage, we can update this csv file daily with a cron job
def get_nasdaq_constituent():
    try:
        url = 'https://financialmodelingprep.com/api/v3/nasdaq_constituent'
        params = {'apikey': api_key}
        r = requests.get(url, params=params)
        df = pd.DataFrame(r.json())
        df.to_csv('nasdaq_constituent.csv', index=False, header=True)
        return True
    except Exception as e:
        return e


df = pd.read_csv('nasdaq_constituent.csv')

tickers = df['symbol'].tolist()

sectors = [ sector for sector in df['sector'].unique() if str(sector) != 'nan']

subSectors = [ subSector for subSector in df['subSector'].unique() if str(subSector) != 'nan']

divided_companies = {sector: df[df['sector'] == sector]['symbol'].tolist() for sector in sectors}

company_names = {company: df[df['symbol'] == company]['name'].tolist()[0] for company in tickers}

class CompanyAnalysis:

    def __init__(self, ticker):
        self.ticker = ticker

    def get_company_financial_statement(self, ticker):
        url = f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=120'
        params = {'apikey': api_key}
        r = requests.get(url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            if not os.path.exists('metrics/income_statement'):
                os.makedirs('metrics/income_statement')
            df.to_csv(f'metrics/income_statement/{ticker}.csv', index=False, header=True)
            return df
        else:
            traceback.print_stack()
            print(r.content)


    def get_company_balance_sheet(self, ticker):
        url = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?limit=120'
        params = {'apikey': api_key}
        r = requests.get(url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            if not os.path.exists('metrics/balance_sheet'):
                os.makedirs('metrics/balance_sheet')
            df.to_csv(f'metrics/balance_sheet/{ticker}.csv', index=False, header=True)
            return df
        else:
            traceback.print_stack()
            print(r.content)
    
    def get_company_cash_flow(self, ticker):
        url = f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?limit=120'
        params = {'apikey': api_key}
        r = requests.get(url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            if not os.path.exists('metrics/cash_flow'):
                os.makedirs('metrics/cash_flow')
            df.to_csv(f'metrics/cash_flow/{ticker}.csv', index=False, header=True)
            return df
        else:
            traceback.print_stack()
            print(r.content)

    def get_company_earning_call(self, ticker):
        url = f'https://financialmodelingprep.com/api/v3/earning_call_transcript?symbol={ticker}'
        params = {'apikey': api_key}
        r = requests.get(url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            if not os.path.exists('metrics/earning_call'):
                os.makedirs('metrics/earning_call')
            df.to_csv(f'metrics/earning_call/{ticker}.csv', index=False, header=True)
            return df
        else:
            traceback.print_stack()
            print(r.content)
    
    def get_company_financial_ratios(self, ticker):
        url = f'https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}'
        params = {'apikey': api_key}
        r = requests.get(url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            if not os.path.exists('metrics/financial_ratios'):
                os.makedirs('metrics/financial_ratios')
            df.to_csv(f'metrics/financial_ratios/{ticker}.csv', index=False, header=True)
            return df
        else:
            traceback.print_stack()
            print(r.content)
        
    def get_company_financial_score(self, ticker):
        url = f'https://financialmodelingprep.com/api/v4/score?symbol={ticker}'
        params = {'apikey': api_key}
        r = requests.get(url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            if not os.path.exists('metrics/financial_score'):
                os.makedirs('metrics/financial_score')
            df.to_csv(f'metrics/financial_score/{ticker}.csv', index=False, header=True)
            return df
        else:
            traceback.print_stack()
            print(r.content)
        
    def get_company_financial_growth(self, ticker):
        url = f'https://financialmodelingprep.com/api/v3/financial-growth/{ticker}?limit=40'
        params = {'apikey': api_key}
        r = requests.get(url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            if not os.path.exists('metrics/financial_growth'):
                os.makedirs('metrics/financial_growth')
            df.to_csv(f'metrics/financial_growth/{ticker}.csv', index=False, header=True)
            return df
        else:
            traceback.print_stack()
            print(r.content)
        
    def get_company_key_metrics(self, ticker):
        url = f'https://financialmodelingprep.com/api/v3/key-metrics-ttm/{ticker}?limit=40'
        params = {'apikey': api_key}
        r = requests.get(url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            if not os.path.exists('metrics/key_metrics'):
                os.makedirs('metrics/key_metrics')
            df.to_csv(f'metrics/key_metrics/{ticker}.csv', index=False, header=True)
            return df
        else:
            traceback.print_stack()
            print(r.content)
    
    def get_company_financial_statement_growth(self, ticker):
        url = f'https://financialmodelingprep.com/api/v3/income-statement-growth/{ticker}?limit=40'
        params = {'apikey': api_key}
        r = requests.get(url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            if not os.path.exists('metrics/financial_statement_growth'):
                os.makedirs('metrics/financial_statement_growth')
            df.to_csv(f'metrics/financial_statement_growth/{ticker}.csv', index=False, header=True)
            return df
        else:
            print(r.content, function.__name__)
        
    def get_company_cash_flow_statement_growth(self, ticker):
        url = f'https://financialmodelingprep.com/api/v3/cash-flow-statement-growth/{ticker}?limit=40'
        params = {'apikey': api_key}
        r = requests.get(url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            if not os.path.exists('metrics/cash_flow_statement_growth'):
                os.makedirs('metrics/cash_flow_statement_growth')
            df.to_csv(f'metrics/cash_flow_statement_growth/{ticker}.csv', index=False, header=True)
            return df
        else:
            traceback.print_stack()
            print(r.content)
    
    def get_company_balance_sheet_statement_growth(self, ticker):
        url = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement-growth/{ticker}?limit=40'
        params = {'apikey': api_key}
        r = requests.get(url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json()) 
            if not os.path.exists('metrics/balance_sheet_statement_growth'):
                os.makedirs('metrics/balance_sheet_statement_growth')
            df.to_csv(f'metrics/balance_sheet_statement_growth/{ticker}.csv', index=False, header=True)
            return df
        else:
            traceback.print_stack()
            print(r.content)
    
    def get_company_profile(self, ticker):
        url = f'https://financialmodelingprep.com/api/v3/profile/{ticker}'
        params = {'apikey': api_key}
        r = requests.get(url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            if not os.path.exists('metrics/profile'):
                os.makedirs('metrics/profile')
            df.to_csv(f'metrics/profile/{ticker}.csv', index=False, header=True)
            return df
        else:
            traceback.print_stack()
            print(r.content)
    
    def get_company_key_executives(self, ticker):
        url = f'https://financialmodelingprep.com/api/v3/key-executives/{ticker}'
        params = {'apikey': api_key}
        r = requests.get(url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json()) 
            if not os.path.exists('metrics/key_executives'):
                os.makedirs('metrics/key_executives')
            df.to_csv(f'metrics/key_executives/{ticker}.csv', index=False, header=True)
            return df
        else:
            traceback.print_stack()
            print(r.content)
        
    def get_company_stock_peers(self, ticker):
        url = f'https://financialmodelingprep.com/api/v4/stock_peers/symbol={ticker}'
        params = {'apikey': api_key}
        r = requests.get(url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            if not os.path.exists('metrics/stock_peers'):
                os.makedirs('metrics/stock_peers')
            df.to_csv(f'metrics/stock_peers/{ticker}.csv', index=False, header=True)
            return df
        else:
            traceback.print_stack()
            print(r.content)
        
    def gather_company_metrics(self):
        ticker = self.ticker
        self.get_company_financial_statement(ticker)
        self.get_company_balance_sheet(ticker)
        self.get_company_cash_flow(ticker)
        self.get_company_earning_call(ticker)
        self.get_company_financial_score(ticker)
        self.get_company_financial_ratios(ticker)
        self.get_company_financial_growth(ticker)
        self.get_company_key_metrics(ticker)
        self.get_company_financial_statement_growth(ticker)
        self.get_company_cash_flow_statement_growth(ticker)
        self.get_company_balance_sheet_statement_growth(ticker)
        self.get_company_profile(ticker)
        self.get_company_key_executives(ticker)
        self.get_company_stock_peers(ticker)
    

# Example on how to use the class:
# ticker = 'AAPL'
# company_analysis = CompanyAnalysis(ticker)
# company_analysis.gather_company_metrics()
