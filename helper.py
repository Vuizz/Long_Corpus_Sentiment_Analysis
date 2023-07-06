articles_website = ['www.barrons.com', 'www.bizjournals.com', 'www.fool.com', 'www.investopedia.com', 'www.marketwatch.com', 'www.realmoney.thestreet.com', 'www.investors.com', 'www.wsj.com', 'www.finance.yahoo.com', 'www.thestreet.com']


from benzinga import financial_data

api_key = '5ab4fd28d6354d719f239c38f276368e'
financial_data = financial_data.Benzinga(api_key)
stock_ratios = financial_data.ratings()
print(financial_data.output(stock_ratios))