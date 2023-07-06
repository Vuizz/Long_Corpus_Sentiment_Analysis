from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from main import tickers
from helper import articles_website
import os
import pandas as pd
from tqdm import tqdm
from termcolor import colored
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing
from time import time
from datetime import datetime

import random

url = 'https://finviz.com/quote.ashx?t='
news_tables = {}
def fetch_news_table(ticker):
    try:
        req = Request(url + ticker + '&p=d', headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req, timeout=10).read()
        soup = BeautifulSoup(html, 'html.parser')
        news_table = soup.find(id='news-table')
        return (ticker, news_table)
    except Exception as e:
        return (ticker, None)

# Make the Pool of workers
available_workers = multiprocessing.cpu_count()
pool = ThreadPool(available_workers)

print('Scraping news tables ...')
news_results = list(tqdm(pool.imap(fetch_news_table, tickers), total=len(tickers)))

# Close the pool and wait for the work to finish
pool.close()
pool.join()

# Separate successful scrapes from failed ones
news_tables = {}
tickers_failed = []
for ticker, news_table in news_results:
    if news_table is not None:
        news_tables[ticker] = news_table
    else:
        tickers_failed.append(ticker)

# Print results
if tickers_failed:
    print(colored('Error: failed to scrape news tables for {}'.format(tickers_failed),'red', attrs=['bold']))
else:
    print(colored(f'Done scraping news tables, {len(news_tables.keys())} tables found. Now parssing ...', 'green', attrs=['bold']))
print('\n')

if os.path.exists('stock_news.csv'):
    parsed_news = pd.read_csv('stock_news.csv').values.tolist()
else:
    parsed_news = []

new_news = 0
keys = news_tables.keys()
new_sources = []
print('Parsing news tables ...')
for ticker in tqdm(keys):
    html_table = news_tables[ticker]
    table_rows = html_table.findAll('tr')
    for index, row in enumerate(table_rows):
        title = row.a.text
        if '[email protected]' in title:
            title = title.replace('[email protected]', '')
        date_data = row.td.text.split(' ')
        if len(date_data) == 21:
            time = date_data[12][:-2]
        else:
            date = date_data[12]
            time = date_data[13][:-2]
        
        link = row.a['href']
        link_source = link.split('https://')[1].split('/')[0]
        source = row.span.text
        if source[0] == '(':
            source = source[1:-1]
        if source[-1] == ')':
            source = source[:-2]
        if 'email protected' in source:
            source = 'None'
        if link_source[0:4] != 'www.':
            link_source = 'www.' + link_source
        if not (link_source in articles_website):
            new_sources.append(link_source)
            articles_website.append(link_source)
            with open('helper.py', 'w') as f:
                f.write(f'articles_website = {articles_website}')
        datetime_str = date + ',' + time
        datetime_obj = datetime.strptime(datetime_str, "%b-%d-%y,%I:%M%p")
        if not any(all(x in sub_array for x in [title, link]) for sub_array in parsed_news):
            article = ''
            error = False
            parsed = False
            parsed_news.append([ticker, datetime_obj, date, time, title, link, source, link_source, article, error, parsed])
            new_news += 1
if new_news == 0:
    print('Done parsing news tables,', colored(f'{new_news} new news found.', 'red', attrs=['bold']))
else:
    print('Done parsing news tables,', colored(f'{new_news} new news found.', 'green', attrs=['bold']), 'Now saving ...')
    if len(new_sources) > 0:
        print(colored(f'New sources found: {new_sources}', 'green', attrs=['bold']))
    print('\n')
    if os.path.exists('stock_news.csv'):
        os.remove('stock_news.csv')
    df = pd.DataFrame(parsed_news, columns=['ticker', 'datetime', 'date', 'time', 'title', 'link', 'source', 'link_source','article', 'error', 'parsed'])
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S')
    df = df.sort_values('datetime', ascending=True)

    df.to_csv('stock_news.csv', index=False, header=True)
    print(colored('Done saving news tables.', 'green', attrs=['bold']))



        

