from urllib.request import urlopen, Request
from urllib.parse import urlencode

import pandas as pd

from bs4 import BeautifulSoup

import requests

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options

from youtube_transcript_api import YouTubeTranscriptApi

from tqdm import tqdm

import os

import textwrap

import re

from termcolor import colored

from helper import articles_website

from errors import missing_source_function

from prettytable import PrettyTable

news_articles = pd.read_csv('stock_news.csv')
link_errors = {}
options = webdriver.EdgeOptions()
options.add_argument("--disable-gpu")
options.add_argument('--log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-logging']) 


def extract_article_yahoo(link):
    try:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('div', 'caas-body')
        continue_reading = soup.find('a', string='Continue reading')
        text = ''
        if article:
            if continue_reading:
                href = continue_reading['href']
                known_sources = article_function_map.keys()
                for source in known_sources:
                    if source in href:
                        return article_function_map[source](href)
                text = 'No extraction function for this domain. Please add one. Link: ' + '@LINK@' + href + '@LINK@'
        paragraphs = article.find_all('p')
        text += '\n'.join([paragraph.text for paragraph in tqdm(paragraphs) if not paragraph.find('a')])
        return text
    except:
        if 'www.finance.yahoo.com' in link_errors.keys():
            link_errors['www.finance.yahoo.com'].append(link)
        else:
            link_errors['www.finance.yahoo.com'] = [link]
        return 'None'


def use_archive_today_barrons(link):
    url = 'https://archive.ph'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    form = soup.find('form', {'id':"submiturl"})
    submit_id = form.find('input', {'name':'submitid'})['value']
    data = {
            "submitid": submit_id,
            "url": link
        }
    params = urlencode(data)
    print('Using Driver to process this article')
    driver = webdriver.Edge(service=Service('C:/Program Files/EdgeDriver/msedgedriver.exe'), options=options)
    driver.get(f'https://archive.ph/submit/?{params}')
    try:
        
        element = WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "center"))
        )
    except:
        pass
    html2 = driver.page_source
    driver.quit()
    soup2 = BeautifulSoup(html2, 'html.parser')
    body = soup2.find('div', {'itemprop':'articleBody'})
    if body:
        article = body.find('section')
        paragraphs = article.findChildren('div', recursive=False)
        text = ''
        for paragraph in tqdm(paragraphs):
            if not paragraph.findChildren('div'):
                text += paragraph.get_text(strip=True, separator=' ') + '\n'
            else:
                child_paragraphs = paragraph.findChildren('div', recursive=False)
                for child_paragraph in child_paragraphs:
                    if 'Newsletter Sign-Up' not in child_paragraph.get_text(strip=True):
                        text += child_paragraph.get_text(strip=True, separator=' ') + '\n'
    else:
        body2 = soup2.find('main', {'style':'box-sizing:border-box;display:block;'})
        second_main = body2.find('main', {'style':'box-sizing:border-box;display:block;grid-column-end:main;grid-column-start:main;grid-row-end:main;grid-row-start:main;'})
        article_body = second_main.find('div', {'style':'align-items:center;box-sizing:border-box;display:flex;flex-direction:column;max-width:620px;padding-block-end:0px;padding-block-start:0px;position:relative;-webkit-box-align:center;width:100%;'})
        article_paragraphs = article_body.find_all('div')
        text = ''   
        for paragraph in tqdm(article_paragraphs):
            if not (paragraph.get_text(strip=True, separator=' ') in text):
                text += paragraph.get_text(strip=True, separator=' ') + '\n'

    return text

def extract_article_barrons(link):
    try:
        text = use_archive_today_barrons(link)
        return text
    except:
        if 'www.barrons.com' in link_errors.keys():
            link_errors['www.barrons.com'].append(link)
        else:
            link_errors['www.barrons.com'] = [link]
        return 'None'

def use_archive_today_bizjournals(link):
    url = 'https://archive.ph'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    form = soup.find('form', {'id':"submiturl"})
    submit_id = form.find('input', {'name':'submitid'})['value']
    data = {
            "submitid": submit_id,
            "url": link
        }
    params = urlencode(data)
    driver = webdriver.Edge(service=Service('C:/Program Files/EdgeDriver/msedgedriver.exe'), options=options)
    driver.get(f'https://archive.ph/submit/?{params}')
    try:
        # Wait up to 5 min for the element to be present
        element = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[id='HEADER']"))
        )
    except:
        pass
    html2 = driver.page_source
    driver.quit()
    soup2 = BeautifulSoup(html2, 'html.parser')
    article_bodies = soup2.find_all(lambda tag: tag.name == 'div' and tag.get('style') and 'Guardian Text Egyptian ACBJ' in tag.get('style'))
    text = ''   
    for paragraph in tqdm(article_bodies):
        if paragraph.get_text(strip=True):
            if paragraph.get_text(strip=True) not in text:
                text += paragraph.get_text(strip=True, separator=' ') + '\n'
    return text    

def extract_article_bizjournals(link):
    try:
        text = use_archive_today_bizjournals(link)
        return text
    except:
        if 'www.bizjournals.com' in link_errors.keys():
            link_errors['www.bizjournals.com'].append(link)
        else:
            link_errors['www.bizjournals.com'] = [link]
        return 'None'

def extract_article_fool(link):
    try:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('div', 'arts__wrapper')
        video_link = article.find('div', 'video-wrapper')
        if video_link:
            video_link = video_link.find('iframe')['src']
            video_id = video_link.split('embed/')[1].split('?')[0]
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            video_text = ''
            for i in tqdm(transcript):
                video_text += i['text'] + ' '
        paragraphs = article.find_all('p')
        text = '\n'.join([paragraph.get_text(strip=True, separator=' ') for paragraph in tqdm(paragraphs)])
        if video_link:
            text += '\n' + video_text
        return text
    except:
        if 'www.fool.com' in link_errors.keys():
            link_errors['www.fool.com'].append(link)
        else:
            link_errors['www.fool.com'] = [link]
        return 'None'

def extract_article_investopedia(link):
    try:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('div', 'comp article-body-content mntl-sc-page mntl-block')
        paragraphs = article.find_all('p')
        text = '\n'.join([paragraph.get_text(strip=True, separator=' ') for paragraph in tqdm(paragraphs)])
        return text
    except:
        if 'www.investopedia.com' in link_errors.keys():
            link_errors['www.investopedia.com'].append(link)
        else:
            link_errors['www.investopedia.com'] = [link]
        return 'None'

def use_archive_today_marketwatch(link):
    url = 'https://archive.ph'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    form = soup.find('form', {'id':"submiturl"})
    submit_id = form.find('input', {'name':'submitid'})['value']
    data = {
            "submitid": submit_id,
            "url": link
        }
    params = urlencode(data)
    print('Using Driver to process this article')
    driver = webdriver.Edge(service=Service('C:/Program Files/EdgeDriver/msedgedriver.exe'), options=options)
    driver.get(f'https://archive.ph/submit/?{params}')
    try:
        
        element = WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "script[id='articleSchemaDefinition']"))
        )
    except:
        pass
    html2 = driver.page_source
    driver.quit()
    soup2 = BeautifulSoup(html2, 'html.parser')
    article_body = soup2.find('article')
    text = ''   
    for paragraph in tqdm(article_body):
        if paragraph.get_text(strip=True):
            if paragraph.get_text(strip=True) not in text:
                text += paragraph.get_text(strip=True, separator=' ') + '\n'
    return text

def extract_article_marketwatch(link):
    try:
        text = use_archive_today_marketwatch(link)
        return text
    except:
        if 'www.marketwatch.com' in link_errors.keys():
            link_errors['www.marketwatch.com'].append(link)
        else:
            link_errors['www.marketwatch.com'] = [link]
        return 'None'

def use_archive_today_realmoney(link):
    url = 'https://archive.ph'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    form = soup.find('form', {'id':"submiturl"})
    submit_id = form.find('input', {'name':'submitid'})['value']
    data = {
            "submitid": submit_id,
            "url": link
        }
    params = urlencode(data)
    print('Using Driver to process this article')
    driver = webdriver.Edge(service=Service('C:/Program Files/EdgeDriver/msedgedriver.exe'), options=options)
    driver.get(f'https://archive.ph/submit/?{params}')
    try:
        
        element = WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[itemprop='articleBody']"))
        )
    except:
        pass
    html2 = driver.page_source
    driver.quit()
    soup2 = BeautifulSoup(html2, 'html.parser')
    article = soup2.find('div', {'itemprop':"articleBody"})
    text = '\n'.join([paragraph.get_text(strip=True, separator=' ') for paragraph in tqdm(article)])
    return text

def extract_article_realmoney(link):
    try:
        text = use_archive_today_realmoney(link)
        return text
    except:
        if 'www.realmoney.thestreet.com' in link_errors.keys():
            link_errors['www.realmoney.thestreet.com'].append(link)
        else:
            link_errors['www.realmoney.thestreet.com'] = [link]
        return 'None'

def extract_article_investors(link):
    try:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('div', {'class':"single-post-content post-content drop-cap crawler"})
        paragraphs = article.find_all('p')
        text = ''
        for paragraph in tqdm(paragraphs):
            if (paragraph.get_text(strip=True) == 'YOU MIGHT ALSO LIKE:') or (paragraph.get_text(strip=True) == 'YOU MAY ALSO LIKE:'):
                break
            else:
                text += paragraph.get_text(strip=True, separator=' ') + '\n'
        return text
    except:
        if 'www.investors.com' in link_errors.keys():
            link_errors['www.investors.com'].append(link)
        else:
            link_errors['www.investors.com'] = [link]
        return 'None'

def use_archive_today_wsj(link):
    url = 'https://archive.ph'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    form = soup.find('form', {'id':"submiturl"})
    submit_id = form.find('input', {'name':'submitid'})['value']
    data = {
            "submitid": submit_id,
            "url": link
        }
    params = urlencode(data)
    print('Using Driver to process this article')
    driver = webdriver.Edge(service=Service('C:/Program Files/EdgeDriver/msedgedriver.exe'), options=options)
    driver.get(f'https://archive.ph/submit/?{params}')
    try:
        
        element = WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "main[id='main']"))
        )
    except:
        pass
    html2 = driver.page_source
    driver.quit()
    soup2 = BeautifulSoup(html2, 'html.parser')
    article = soup2.find('main', {'id':"main"})
    text = '\n'.join([paragraph.get_text(strip=True, separator=' ') for paragraph in tqdm(article)])
    return text

def extract_article_wsj(link):
    try:
        text = use_archive_today_wsj(link)
        return text
    except:
        if 'www.wsj.com' in link_errors.keys():
            link_errors['www.wsj.com'].append(link)
        else:
            link_errors['www.wsj.com'] = [link]
        return 'None'


def extract_article_thestreet(link):
    try:
        url = 'https://archive.ph'
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        form = soup.find('form', {'id':"submiturl"})
        submit_id = form.find('input', {'name':'submitid'})['value']
        data = {
        "submitid": submit_id,
        "url": link
        }
        params = urlencode(data)
        print('Using Driver to extract this article... This might take some time.')
        driver = webdriver.Edge(service=Service('C:/Program Files/EdgeDriver/msedgedriver.exe'), options=options)
        driver.get(f'https://archive.ph/submit/?{params}')
        try:
            
            element = WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "header[style='box-sizing:border-box;display:block;']"))
            )
        except:
            pass
        html2 = driver.page_source
        driver.quit()
        soup2 = BeautifulSoup(html2, 'html.parser')
        article = soup2.find('header', {'style':"box-sizing:border-box;display:block;"})
        article = article.find_parent('div')
        paragraphs = article.findChildren('div', recursive=False)
        text = ''
        for paragraph in tqdm(paragraphs):
            if (paragraph.get_text(strip=True) not in text) and (paragraph.text != ''):
                text += paragraph.get_text(strip=True, separator=' ') + '\n'
        return text
    except:
        if 'www.thestreet.com' in link_errors.keys():
            link_errors['www.thestreet.com'].append(link)
        else:
            link_errors['www.thestreet.com'] = [link]
        return 'None'

article_function_map = {
    'www.finance.yahoo.com': extract_article_yahoo,
    'www.barrons.com': extract_article_barrons,
    'www.bizjournals.com': extract_article_bizjournals,
    'www.fool.com': extract_article_fool,
    'www.investopedia.com': extract_article_investopedia,
    'www.marketwatch.com': extract_article_marketwatch,
    'www.realmoney.thestreet.com': extract_article_realmoney,
    'www.investors.com': extract_article_investors,
    'www.wsj.com': extract_article_wsj,
    'www.thestreet.com': extract_article_thestreet
}

def extract_article(link, domain):
    if domain in article_function_map.keys():
        return article_function_map[domain](link)
    else:
        return f'No extraction function for this domain. Please add one. \nDomain: {domain}'

def clean_domain(text):
    domain = text.split('://')[1]
    if 'https://' in domain:
        domain = domain.split('https://')[1]
    website = domain.split('/')[0]
    return website

def extract_articles():
    df = pd.read_csv('stock_news.csv')
    links = df[(df['parsed'] == False) | (df['error'] == True)]['link'].tolist()
    # reverse the list links
    links.reverse()
    links = links[0:1]
    missed_links = []
    for link in links:
        
        ticker = df.loc[df['link'] == link, 'ticker'].tolist()[0]
        title = df.loc[df['link'] == link, 'title'].tolist()[0]
        domain = df.loc[df['link'] == link, 'link_source'].tolist()[0]
        datetime = df.loc[df['link'] == link, 'datetime'].tolist()[0]
        datetime = datetime.replace(':', '_').replace('-', '_')
        table = PrettyTable()
        table.field_names = ['Date','Ticker', 'Title']
        table.add_row([datetime, ticker, title])
        print('Preparing to extract the following article:')
        print(table)
        folder = 'articles/' + ticker
        article = extract_article(link, domain).lower()
        if not os.path.exists(folder):
            os.makedirs(folder)
        link_to_article = folder + '/' + datetime + '.txt'
        # Remove non-ASCII characters
        article = re.sub(r'[^\x00-\x7F]+', ' ', article)
        wrapped_article = textwrap.fill(article, width=100)
        with open(link_to_article, 'w') as f:
            f.write(wrapped_article)
        error = False
        if 'No extraction function for this domain. Please add one.' in article:
            print(colored('Error extracting article, no function for this domain', 'red'))
            source_link = article.split('@LINK@')[1].split('@LINK@')[0]
            source = clean_domain(source_link)
            if source not in articles_website:
                articles_website.append(source)
                with open('helper.py', 'w') as f:
                    f.write(f'articles_website = {articles_website}')
            error = True
            missed_links.append(source)
        if article == 'None':
            print(colored('Error extracting article', 'red'))
            error = True
        existing_functions = article_function_map.keys()

        if (article != 'None') and ('No extraction function for this domain. Please add one.' not in article):
            print(colored('Article extracted successfully', 'green'))
        
        print('\n')

        diff = [item for item in articles_website if item not in existing_functions]
        update_file = False
        for item in diff:
            if item not in missing_source_function:
                missing_source_function.append(item)
                update_file = True
        
        with open('errors.py', 'w') as f:
            f.write(f'missing_source_function = {missing_source_function}')
        
        df.loc[df['link'] == link, 'article'] = link_to_article
        df.loc[df['link'] == link, 'error'] = error
        # Change below to True when not testing
        df.loc[df['link'] == link, 'parsed'] = True
        df.to_csv('stock_news.csv', index=False)
    
    print('\n')

    if len(links) == 0:
        print(colored('No new articles to extract', 'orange', attrs=['bold']))
    elif len(links) == 1:
        if len(link_errors.keys()) > 0 or len(missed_links) > 0:
            print(colored(f'Finished extracting {len(links)} article, with {len(link_errors.keys()) + len(missed_links)} errors', 'red', attrs=['bold']))
        else:  
            print(colored(f'Finished extracting {len(links)} article', 'green', attrs=['bold']))
    else:
        if len(link_errors.keys()) > 0 or len(missed_links) > 0:
            print(colored(f'Finished extracting {len(links)} articles with {len(link_errors.keys()) + len(missed_links)} errors', 'red', attrs=['bold']))
        else:
            print(colored(f'Finished extracting {len(links)} articles', 'green', attrs=['bold']))
    if len(link_errors.keys()) > 0:
        print(colored('The following links had errors: ', 'red', attrs=['bold']))
        for key in link_errors.keys():
            print(colored(f'Domain: {key}', 'red', attrs=['bold']))
            for link in link_errors[key]:
                print(colored(f'Link: {link}', 'red', attrs=['bold']))
    else:
        print(colored('No errors', 'green', attrs=['bold']))

    if len(missed_links) > 0:
        print(colored('The following links were not extracted, missing source extraction function: ', 'red', attrs=['bold']))
        for link in missed_links:
            print(colored(f'Source: {link}', 'red', attrs=['bold']))

extract_articles()


