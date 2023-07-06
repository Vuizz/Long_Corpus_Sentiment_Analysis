import os

import pandas as pd


class Company:

    def __init__(self, name):
        self.name = name
        self.financials = {}
        self.news_articles = []
        self.metrics = {}
        self.financial_statements()
        self.add_article()
        self.analyze_balance_sheet()
        self.analyze_balance_sheet_growth()
        self.analyze_cash_flow()
        self.analyze_cash_flow_growth()
        self.analyze_financial_growth()
        self.analyze_financial_ratios()
        self.analyze_financial_statement_growth()
        self.analyze_income_statement()
        self.analyze_key_metrics()
        self.analyze_profile()


    def add_article(self):
        df = pd.read_csv('stock_news.csv')
        articles = df.loc[(df['ticker'] == self.name) & (df['parsed'] == True)][['title', 'ticker', 'article']].values.tolist()
        for article in articles:
            if article not in self.news_articles:
                self.news_articles.append(article)

    def financial_statements(self):
        datapoints = {}
        metrics = os.listdir('metrics')
        for metric in metrics:
            datapoint = {}
            df = pd.read_csv(f'metrics/{metric}/{self.name}.csv')
            df = df.iloc[0].to_dict()
            for key, value in df.items():
                datapoint[key] = value
            datapoints[metric] = datapoint
        
        self.financials = datapoints


    def analyze_balance_sheet(self):
        # Extracting necessary data
        total_assets = self.financials['balance_sheet']['totalAssets']
        total_liabilities = self.financials['balance_sheet']['totalLiabilities']
        total_equity = self.financials['balance_sheet']['totalEquity']
        total_debt = self.financials['balance_sheet']['totalDebt']
        net_receivables = self.financials['balance_sheet']['netReceivables']
        inventory = self.financials['balance_sheet']['inventory']
        total_current_assets = self.financials['balance_sheet']['totalCurrentAssets']
        total_current_liabilities = self.financials['balance_sheet']['totalCurrentLiabilities']
        
        # Calculate financial ratios
        try:
            debt_ratio = total_debt / total_assets
            equity_ratio = total_equity / total_assets
            debt_equity_ratio = total_debt / total_equity
            receivables_turnover = net_receivables / total_assets
            inventory_turnover = inventory / total_assets
            current_ratio = total_current_assets / total_current_liabilities
        except ZeroDivisionError:
            print('Divide by zero error, check if total assets, total equity or total current liabilities are zero.')
        
        debt_ratio_des = "This is a measure of financial leverage, demonstrating a company's total debt as a percentage of its total assets. A high ratio could indicate that the company is heavily financed by debt and may carry a higher risk of default. However, it might be acceptable in capital-intensive industries where companies regularly have high amounts of debt. Always compare this ratio with other companies in the same industry."

        equity_ratio_des = "Also known as a net assets ratio, it is the proportion of the total assets of a company that are financed or owned by the shareholders. This ratio provides insight into the company's financial structure and its dependence on debt for its operations. A higher ratio usually indicates less financial risk because the company has fewer liabilities. However, it might also mean the company is not taking advantage of the increased profits that financial leverage can bring."

        debt_equity_ratio_des = "This ratio is another measure of financial leverage. The debt-to-equity ratio measures the proportion of equity and debt the company is using to finance its assets, and the degree of protection to creditors in the event of a business decline. A high ratio generally means that a company has been aggressive in financing its growth with debt, which can result in volatile earnings. Conversely, a low ratio might indicate less risk but could also suggest that the company is not taking full advantage of the profits that financial leverage can bring."

        receivables_turnover_des = "This ratio quantifies a firm's effectiveness in extending credit and collecting debts. The receivables turnover ratio is an activity ratio, measuring how efficiently a firm uses its assets. A higher ratio indicates that the company collects its receivables more quickly, which is generally positive as it means the company has cash more frequently to use for operations or investments. However, if the ratio is too high, it might mean that the company has a strict credit policy, which could affect sales."

        inventory_turnover_des = "This ratio shows how many times a company's inventory is sold and replaced over a certain period (often one year). A low turnover implies poor sales and, therefore, excess inventory, which can result in high storage costs and obsolescence. Conversely, a high ratio implies either strong sales or insufficient inventory. Insufficient inventory could lead to lost sales and customer dissatisfaction."

        current_ratio_des = "This ratio is a liquidity ratio that measures a company's ability to pay off its short-term liabilities with its short-term assets. A current ratio greater than one indicates that the company can pay off its obligations, which is generally good for financial health. However, a very high ratio could indicate that the company is not efficiently using its current assets or short-term financing facilities. Ratios under one indicate that the company cannot currently pay off its obligations, which might raise concerns about financial stability."

        # Store ratios in a dictionary
        financial_ratios = {
            'debt_ratio': [debt_ratio, debt_ratio_des],
            'equity_ratio': [equity_ratio, equity_ratio_des],
            'debt_equity_ratio': [debt_equity_ratio, debt_equity_ratio_des],
            'receivables_turnover': [receivables_turnover, receivables_turnover_des],
            'inventory_turnover': [inventory_turnover, inventory_turnover_des],
            'current_ratio': [current_ratio, current_ratio_des]
        }

        self.metrics['balance_sheet'] = financial_ratios

    def analyze_balance_sheet_growth(self):
        # Extract necessary data
        growth_total_assets = self.financials['balance_sheet_statement_growth']['growthTotalAssets']
        growth_total_equity = self.financials['balance_sheet_statement_growth']['growthTotalStockholdersEquity']
        growth_total_liabilities = self.financials['balance_sheet_statement_growth']['growthTotalLiabilities']
        growth_total_debt = self.financials['balance_sheet_statement_growth']['growthTotalDebt']
        growth_net_receivables = self.financials['balance_sheet_statement_growth']['growthNetReceivables']
        growth_inventory = self.financials['balance_sheet_statement_growth']['growthInventory']
        growth_total_current_assets = self.financials['balance_sheet_statement_growth']['growthTotalCurrentAssets']
        growth_total_current_liabilities = self.financials['balance_sheet_statement_growth']['growthTotalCurrentLiabilities']
        growth_long_term_debt = self.financials['balance_sheet_statement_growth']['growthLongTermDebt']

        # Store growth metrics in a dictionary

        des_growth_total_assets = "The rate of growth of the company's total assets. A consistently positive value could indicate a successful growth strategy. However, if the growth in assets is largely driven by increased borrowing, it might be a warning sign of financial distress. Comparing this with growth in equity and liabilities provides a fuller picture of the company's financial health."

        des_growth_total_equity = "This measures the rate of growth in shareholders' equity. Growth in shareholders' equity could indicate that the company is becoming more valuable to shareholders. A consistently high growth rate can suggest that the company is consistently generating profits and reinvesting them back into the business. It's a positive sign of the company's long-term financial stability."

        des_growth_total_liabilities = "This measures the rate of growth in the company's total liabilities. If these are growing faster than assets or equity, it could indicate increased financial risk. A high rate of growth in liabilities, especially when paired with relatively slow growth in assets or equity, could be a red flag indicating potential solvency issues in the future."

        des_growth_total_debt = des_growth_total_liabilities

        des_growth_net_receivables = "This measures the rate of growth in the company's net receivables, which are the money owed to the company by its customers. High growth in these categories could indicate increased sales activity, which is positive. However, if this growth is due to the company not collecting payments efficiently, it might be a sign of poor cash management."

        des_growthInventory = "This is the growth rate in the value of the goods or materials a company currently has that it plans to sell. Growth in inventory could be a positive sign if sales are expected to increase in the future. However, if it's growing faster than sales, it could be a negative sign as it might indicate products are not selling as quickly as expected, tying up capital in unsold inventory."

        des_growthTotalCurrentAssets = "This is the growth rate in the total value of all assets that are expected to be converted into cash within one year. An increase could indicate the company is generating more cash or other current assets. However, if current liabilities are also increasing at a faster rate, it may not be a positive sign, as it suggests the company is accumulating short-term obligations that could strain its liquidity."

        des_growthTotalCurrentLiabilities = "This is the growth rate in the total value of all obligations expected to be paid by the company within one year. A large increase in current liabilities could suggest a company is taking on short-term debt to finance its operations, which might increase financial risk if not managed properly. It's important to monitor this in relation to current assets to assess the company's ability to meet its short-term obligations."

        des_growthLongTermDebt = "This is the growth rate in the total value of debt that is due more than one year in the future. An increase in long-term debt could suggest that the company is investing in long-term projects, which could be a good sign if those investments yield high returns. However, if the growth in long-term debt is consistent and significantly high, it could indicate that the company is struggling with cash flow and relying on debt to finance operations, which could increase financial risk."

        growth_metrics = {
            'growth_total_assets' : [growth_total_assets , des_growth_total_assets],
            'growth_total_equity': [growth_total_equity, des_growth_total_equity],
            'growth_total_liabilities': [growth_total_liabilities, des_growth_total_liabilities],
            'growth_total_debt': [growth_total_debt, des_growth_total_debt],
            'growth_net_receivables': [growth_net_receivables, des_growth_net_receivables],
            'growth_inventory': [growth_inventory, des_growthInventory],
            'growth_total_current_assets': [growth_total_current_assets, des_growthTotalCurrentAssets],
            'growth_total_current_liabilities': [growth_total_current_liabilities, des_growthTotalCurrentLiabilities],
            'growth_long_term_debt': [growth_long_term_debt, des_growthLongTermDebt]
        }

        self.metrics['balance_sheet_growth'] = growth_metrics

    def analyze_cash_flow(self):
        # Extracting necessary data
        net_income = self.financials['cash_flow']['netIncome']
        operating_cash_flow = self.financials['cash_flow']['operatingCashFlow']
        capital_expenditure = self.financials['cash_flow']['capitalExpenditure']
        free_cash_flow = self.financials['cash_flow']['freeCashFlow']
        net_cash_used_for_investing_activities = self.financials['cash_flow']['netCashUsedForInvestingActivites']
        net_cash_used_provided_by_financing_activities = self.financials['cash_flow']['netCashUsedProvidedByFinancingActivities']

        # Calculate financial metrics
        try:
            operating_cash_flow_margin = operating_cash_flow / net_income
            capex_as_percentage_of_sales = capital_expenditure / net_income
            free_cash_flow_margin = free_cash_flow / net_income
            investing_cash_flow_margin = net_cash_used_for_investing_activities / net_income
            financing_cash_flow_margin = net_cash_used_provided_by_financing_activities / net_income
        except ZeroDivisionError:
            print('Divide by zero error, check if net income is zero.')

        operating_cash_flow_margin_des = "This is a profitability ratio that measures how well a company turns sales into cash. It's calculated by dividing operating cash flow by net sales. The higher the percentage, the better, as it means the company is doing well at generating cash to pay bills, fund operations, and make investments. An increasing trend over time indicates improving operational efficiency."

        capex_as_percentage_of_sales_des = "Capital expenditure (CapEx) is the money an organization spends to buy, maintain, or improve its fixed assets such as property, plant and equipment. Tracking CapEx as a percentage of sales provides insight into a company's investment strategy. A high ratio might indicate that the company is investing heavily in future growth. However, if this ratio is significantly higher than other companies in the same industry, it could indicate that the company is over-investing or not spending efficiently."

        free_cash_flow_margin_des = "Free Cash Flow Margin is a measure of the percentage of revenue left over after the company has paid for its operating expenses and capital expenditures. It tells us the cash that a company is able to generate after spending the money required to maintain or expand its asset base. A higher ratio is generally better and it indicates the company has more cash available for shareholders, debt repayment, and acquisitions."

        investing_cash_flow_margin_des = "Investing Cash Flow Margin gives us an idea about a company's investing activities in relation to its sales. A negative ratio could mean the company is investing more into its business, which might be good for future growth. A positive ratio could mean the company is divesting assets. It's important to compare this ratio with peers in the industry to understand if the company's investment strategy is in line with the industry norms."

        financing_cash_flow_margin_des = "Financing Cash Flow Margin measures the net cash from financing activities as a percentage of a company’s total revenues. A positive ratio might indicate the company is raising more capital, while a negative ratio could mean that the company is paying down debt, paying dividends, or buying back stock. Both can be seen as positive, depending on the company's strategy and the market's expectations."



        # Store metrics in a dictionary
        cash_flow_metrics = {
            'operating_cash_flow_margin': [operating_cash_flow_margin, operating_cash_flow_margin_des],
            'capex_as_percentage_of_sales': [capex_as_percentage_of_sales, capex_as_percentage_of_sales_des],
            'free_cash_flow_margin': [free_cash_flow_margin, free_cash_flow_margin_des],
            'investing_cash_flow_margin': [investing_cash_flow_margin, investing_cash_flow_margin_des],
            'financing_cash_flow_margin': [financing_cash_flow_margin, financing_cash_flow_margin_des]
        }

        self.metrics['cash_flow'] = cash_flow_metrics

    def analyze_cash_flow_growth(self):
        # Extracting necessary data
        growth_net_income = self.financials['cash_flow_statement_growth']['growthNetIncome']
        growth_operating_cash_flow = self.financials['cash_flow_statement_growth']['growthOperatingCashFlow']
        growth_capital_expenditure = self.financials['cash_flow_statement_growth']['growthCapitalExpenditure']
        growth_free_cash_flow = self.financials['cash_flow_statement_growth']['growthFreeCashFlow']
        growth_net_cash_used_for_investing_activities = self.financials['cash_flow_statement_growth']['growthNetCashUsedForInvestingActivites']
        growth_net_cash_used_provided_by_financing_activities = self.financials['cash_flow_statement_growth']['growthNetCashUsedProvidedByFinancingActivities']

        # Descriptions
        growth_net_income_des =  "This ratio shows how much the company's net income has grown in the given period. Net income is the profit a company has earned for a certain period. A positive growth rate suggests that the company's profits are increasing, which is generally a good sign. Conversely, a negative growth rate may indicate declining profitability."
        growth_operating_cash_flow_des = "This ratio indicates the growth in the cash generated from operating activities in the given period. Operating activities include any sources and uses of cash from business operations. A high and increasing ratio over time is generally positive, indicating that the company is generating more cash from its operations."
        growth_capital_expenditure_des = "This ratio shows the growth in the company's capital expenditure in the given period. Capital expenditures are the funds used by a company to acquire or upgrade physical assets such as property, industrial buildings or equipment. This is essential for maintaining and growing the business. A higher ratio could suggest the company is investing more in its future, but it could also mean lower free cash flows in the short term."
        growth_free_cash_flow_des = "This ratio reveals the growth in the company's free cash flow in the given period. Free cash flow is the cash that a company is able to generate after the money required to maintain or expand its asset base. A higher growth ratio generally indicates a healthy and potentially growing company, since it suggests the company is generating more cash that can be used for reinvestment or returned to shareholders."
        growth_net_cash_used_for_investing_activities_des = "This ratio gives an idea of the growth in the company's cash used for investing activities in the given period. Investing activities include purchase or sale of an asset, loans made to vendors or received from customers or any payments related to a merger or acquisition. A higher ratio could indicate the company is investing more in its future, but could also imply less cash available for other uses."
        growth_net_cash_used_provided_by_financing_activities_des = "This ratio indicates the growth in the company's cash used or provided by financing activities in the given period. Financing activities include the inflow of cash from investors such as banks and shareholders, as well as the outflow of cash to shareholders as dividends. A higher positive ratio might indicate the company is raising more capital, while a higher negative ratio could indicate the company is returning more capital to shareholders or reducing its debt."

        # Store metrics and their descriptions in a dictionary
        cash_flow_growth_metrics = {
            'growth_net_income': [growth_net_income, growth_net_income_des],
            'growth_operating_cash_flow': [growth_operating_cash_flow, growth_operating_cash_flow_des],
            'growth_capital_expenditure': [growth_capital_expenditure, growth_capital_expenditure_des],
            'growth_free_cash_flow': [growth_free_cash_flow, growth_free_cash_flow_des],
            'growth_net_cash_used_for_investing_activities': [growth_net_cash_used_for_investing_activities, growth_net_cash_used_for_investing_activities_des],
            'growth_net_cash_used_provided_by_financing_activities': [growth_net_cash_used_provided_by_financing_activities, growth_net_cash_used_provided_by_financing_activities_des]
        }

        self.metrics['cash_flow_statement_growth'] = cash_flow_growth_metrics

    def analyze_financial_growth(self):
        # Extracting necessary data
        revenue_growth = self.financials['financial_growth']['revenueGrowth']
        net_income_growth = self.financials['financial_growth']['netIncomeGrowth']
        operating_income_growth = self.financials['financial_growth']['operatingIncomeGrowth']
        eps_growth = self.financials['financial_growth']['epsgrowth']
        free_cash_flow_growth = self.financials['financial_growth']['freeCashFlowGrowth']
        debt_growth = self.financials['financial_growth']['debtGrowth']
        ten_yr_revenue_growth_per_share = self.financials['financial_growth']['tenYRevenueGrowthPerShare']
        five_yr_revenue_growth_per_share = self.financials['financial_growth']['fiveYRevenueGrowthPerShare']
        three_yr_revenue_growth_per_share = self.financials['financial_growth']['threeYRevenueGrowthPerShare']

        # Descriptions
        revenue_growth_des = "This ratio measures the percentage increase in the company's sales over a specific period. A consistently high revenue growth rate is generally seen as a positive sign, suggesting the company is successfully capturing more market share or introducing successful new products. However, it's important to also consider the associated costs of this growth."
        net_income_growth_des = "This ratio shows the percentage increase in the company's net income (after all expenses and taxes) over a specific period. An increasing net income growth rate generally suggests improved profitability, possibly due to operational efficiencies, cost control, or increasing sales. Conversely, a declining growth rate could signal operational or financial challenges."
        operating_income_growth_des = "This ratio represents the growth in income derived from the company's core business operations, not including interest and taxes, over a specific period. Consistent growth in operating income could suggest the company's core business is strong. However, if this growth is not aligned with net income growth, it may imply the company has high non-operating expenses or tax burdens."
        eps_growth_des = "This ratio indicates the percentage growth in the company's earnings per share (EPS) over a specific period. Rising EPS growth could indicate increasing profitability or effective share buybacks. However, it's important to consider if EPS growth is being driven by genuine profitability improvements or financial engineering."
        free_cash_flow_growth_des = "This ratio shows the growth in the company's free cash flow over a specific period. An increasing free cash flow growth rate suggests that the company is generating more cash than it uses for expenditures. This could provide opportunities for investing in growth, paying down debt, or returning money to shareholders."
        debt_growth_des = "This ratio indicates the growth in the company's total debt over a specific period. Increasing debt growth can indicate that a company is fueling growth or operations through borrowing. While debt can provide resources for expansion, high debt growth rates relative to income or cash flow growth may signal unsustainable financial risk."
        ten_yr_revenue_growth_per_share_des = "This ratio shows the compounded annual growth rate of the company's revenue per share over the past ten years. This long-term perspective can provide insights into the sustainability of a company's growth. If this growth rate is declining, it may indicate that the company's growth is slowing."
        five_yr_revenue_growth_per_share_des = "This ratio shows the compounded annual growth rate of the company's revenue per share over the past five years. This mid-term perspective can help identify trends in the company's growth rate and strategic effectiveness."
        three_yr_revenue_growth_per_share_des = "This ratio shows the compounded annual growth rate of the company's revenue per share over the past three years. This shorter-term perspective can help identify more recent trends in the company's growth rate and responsiveness to market changes."

        # Store metrics and their descriptions in a dictionary
        financial_growth_metrics = {
            'revenue_growth': [revenue_growth, revenue_growth_des],
            'net_income_growth': [net_income_growth, net_income_growth_des],
            'operating_income_growth': [operating_income_growth, operating_income_growth_des],
            'eps_growth': [eps_growth, eps_growth_des],
            'free_cash_flow_growth': [free_cash_flow_growth, free_cash_flow_growth_des],
            'debt_growth': [debt_growth, debt_growth_des],
            'ten_yr_revenue_growth_per_share': [ten_yr_revenue_growth_per_share, ten_yr_revenue_growth_per_share_des],
            'five_yr_revenue_growth_per_share': [five_yr_revenue_growth_per_share, five_yr_revenue_growth_per_share_des],
            'three_yr_revenue_growth_per_share': [three_yr_revenue_growth_per_share, three_yr_revenue_growth_per_share_des]
        }

        self.metrics['financial_growth'] = financial_growth_metrics

    
    def analyze_financial_ratios(self):
        # Extracting necessary data
        pe_ratio = self.financials['financial_ratios']['peRatioTTM']
        current_ratio = self.financials['financial_ratios']['currentRatioTTM']
        quick_ratio = self.financials['financial_ratios']['quickRatioTTM']
        debt_ratio = self.financials['financial_ratios']['debtRatioTTM']
        return_on_equity = self.financials['financial_ratios']['returnOnEquityTTM']
        gross_profit_margin = self.financials['financial_ratios']['grossProfitMarginTTM']

        # Descriptions and Analytical Considerations
        pe_ratio_des = "The Price to Earnings (P/E) ratio is a valuation ratio of a company's current share price compared to its per-share earnings. A high P/E ratio could mean that a company's stock is over-valued, or else that investors are expecting high growth rates in the future."
        current_ratio_des = "The current ratio is a liquidity ratio that measures a company's ability to pay short-term and long-term obligations. A current ratio under 1 indicates that the company may have problems meeting its short-term obligations."
        quick_ratio_des = "The quick ratio measures a company's ability to meet its short-term obligations with its most liquid assets. If this ratio is not at least 1.0, it means a company's liquid assets are less than its current liabilities and it could have trouble paying back its immediate liabilities."
        debt_ratio_des = "The debt ratio is a financial ratio that measures the extent of a company's leverage. The debt ratio is defined as the ratio of total debt to total assets, expressed in percentage, it provides an indication of a company's financial risk. A high debt ratio means high borrowing and financial risk."
        return_on_equity_des = "The Return on Equity (ROE) is a measure of financial performance that calculates the return on investment of shareholders' equity, i.e., the net income returned as a percentage of shareholders equity. ROE measures a company's profitability by revealing how much profit a company generates with the money shareholders have invested."
        gross_profit_margin_des = "The Gross Profit Margin is a financial metric used to assess a company's financial health and business model by revealing the proportion of money left over from revenues after accounting for the cost of goods sold. A high Gross Profit Margin indicates that the company can make a reasonable profit on sales, as long as it keeps overhead costs in control."

        # Store metrics and their descriptions in a dictionary
        financial_ratio_metrics = {
            'pe_ratio': [pe_ratio, pe_ratio_des],
            'current_ratio': [current_ratio, current_ratio_des],
            'quick_ratio': [quick_ratio, quick_ratio_des],
            'debt_ratio': [debt_ratio, debt_ratio_des],
            'return_on_equity': [return_on_equity, return_on_equity_des],
            'gross_profit_margin': [gross_profit_margin, gross_profit_margin_des]
        }

        self.metrics['financial_ratios'] = financial_ratio_metrics

    def analyze_financial_statement_growth(self):
        # Extracting necessary data
        growth_revenue = self.financials['financial_statement_growth']['growthRevenue']
        growth_cost_of_revenue = self.financials['financial_statement_growth']['growthCostOfRevenue']
        growth_gross_profit = self.financials['financial_statement_growth']['growthGrossProfit']
        growth_operating_expenses = self.financials['financial_statement_growth']['growthOperatingExpenses']
        growth_net_income = self.financials['financial_statement_growth']['growthNetIncome']
        growth_eps = self.financials['financial_statement_growth']['growthEPS']

        # Descriptions and Analytical Considerations
        growth_revenue_des = "This metric represents the growth in the company's revenue. Increasing revenue growth generally indicates that the company is growing and is capable of generating more sales."
        growth_cost_of_revenue_des = "This represents the growth in the company's cost of revenue. An increasing trend may indicate that the company's cost to generate revenue is increasing, which may impact the profitability."
        growth_gross_profit_des = "This represents the growth in the company's gross profit. An increasing trend may indicate that the company is becoming more profitable."
        growth_operating_expenses_des = "This represents the growth in the company's operating expenses. An increasing trend may indicate that the company's operational efficiency is declining, which can impact the profitability."
        growth_net_income_des = "This represents the growth in the company's net income. An increasing trend generally indicates that the company is becoming more profitable."
        growth_eps_des = "This represents the growth in the company's Earnings Per Share (EPS). An increasing trend is generally seen as a positive sign, as it indicates that the company is becoming more profitable on a per share basis."

        # Store metrics and their descriptions in a dictionary
        financial_growth_metrics = {
            'growth_revenue': [growth_revenue, growth_revenue_des],
            'growth_cost_of_revenue': [growth_cost_of_revenue, growth_cost_of_revenue_des],
            'growth_gross_profit': [growth_gross_profit, growth_gross_profit_des],
            'growth_operating_expenses': [growth_operating_expenses, growth_operating_expenses_des],
            'growth_net_income': [growth_net_income, growth_net_income_des],
            'growth_eps': [growth_eps, growth_eps_des]
        }

        self.metrics['financial_growth'] = financial_growth_metrics

    def analyze_income_statement(self):
        # Extracting necessary data
        revenue = self.financials['income_statement']['revenue']
        gross_profit = self.financials['income_statement']['grossProfit']
        gross_profit_ratio = self.financials['income_statement']['grossProfitRatio']
        operating_expenses = self.financials['income_statement']['operatingExpenses']
        operating_income = self.financials['income_statement']['operatingIncome']
        operating_income_ratio = self.financials['income_statement']['operatingIncomeRatio']
        net_income = self.financials['income_statement']['netIncome']
        net_income_ratio = self.financials['income_statement']['netIncomeRatio']
        eps = self.financials['income_statement']['eps']

        # Descriptions and Analytical Considerations
        revenue_des = "Revenue is the total income generated by the sale of goods or services related to the company's core operations. It serves as a measure of the company's size and market dominance."
        gross_profit_des = "Gross Profit is the profit a company makes after deducting the costs associated with making and selling its products or providing its services. The gross profit margin ratio gives an indication of the company's profitability."
        operating_expenses_des = "Operating Expenses are the costs associated with a company's normal business operations. It's crucial to keep these as low as possible to maintain profitability."
        operating_income_des = "Operating Income is the profit realized from a business's operations. The operating income ratio gives an indication of the company's operating efficiency and profitability."
        net_income_des = "Net Income is the total profit the company has made after all expenses and taxes. The net income ratio gives an indication of the company's overall profitability after all expenses."
        eps_des = "Earnings per Share (EPS) is a portion of a company's profit divided by the number of outstanding shares. A higher EPS indicates more value because investors will pay more for a company's shares if they think the company has higher profits relative to its share price."

        # Store metrics and their descriptions in a dictionary
        income_statement_metrics = {
            'revenue': [revenue, revenue_des],
            'gross_profit': [gross_profit, gross_profit_des],
            'gross_profit_ratio': [gross_profit_ratio, gross_profit_des],
            'operating_expenses': [operating_expenses, operating_expenses_des],
            'operating_income': [operating_income, operating_income_des],
            'operating_income_ratio': [operating_income_ratio, operating_income_des],
            'net_income': [net_income, net_income_des],
            'net_income_ratio': [net_income_ratio, net_income_des],
            'eps': [eps, eps_des]
        }

        self.metrics['income_statement'] = income_statement_metrics

    def analyze_key_metrics(self):
        # Extracting necessary data
        pe_ratio = self.financials['key_metrics']['peRatioTTM']
        ev_to_sales = self.financials['key_metrics']['evToSalesTTM']
        roe = self.financials['key_metrics']['roeTTM']
        debt_to_equity = self.financials['key_metrics']['debtToEquityTTM']
        current_ratio = self.financials['key_metrics']['currentRatioTTM']

        # Descriptions and Analytical Considerations
        pe_ratio_des = "The Price to Earnings (P/E) ratio is a valuation ratio of a company's current share price compared to its per-share earnings. A high P/E ratio could mean that a company's stock is over-valued, or else that investors are expecting high growth rates in the future."
        ev_to_sales_des = "The Enterprise Value to Sales ratio (EV/Sales) measures the total company value (including market cap and debt) relative to its sales. A low ratio could indicate that the company is undervalued."
        roe_des = "Return on Equity (ROE) measures the profitability of a corporation by revealing how much profit a company generates with the money shareholders have invested. A high ROE indicates a more profitable company."
        debt_to_equity_des = "The Debt to Equity ratio (D/E) is a financial leverage ratio that indicates the proportion of shareholders' equity and debt used to finance the company's assets. A high D/E ratio generally means that a company has been aggressive in financing its growth with debt."
        current_ratio_des = "The Current Ratio is a liquidity ratio that measures a company's ability to pay short-term obligations. A ratio under 1 indicates that the company would be unable to pay off its obligations if they came due at that point."

        # Store metrics and their descriptions in a dictionary
        key_financial_metrics = {
            'pe_ratio': [pe_ratio, pe_ratio_des],
            'ev_to_sales': [ev_to_sales, ev_to_sales_des],
            'roe': [roe, roe_des],
            'debt_to_equity': [debt_to_equity, debt_to_equity_des],
            'current_ratio': [current_ratio, current_ratio_des]
        }

        self.metrics['key_metrics'] = key_financial_metrics

    def analyze_profile(self):
        # Extracting necessary data
        symbol = self.financials['profile']['symbol']
        price = self.financials['profile']['price']
        beta = self.financials['profile']['beta']
        mkt_cap = self.financials['profile']['mktCap']
        vol_avg = self.financials['profile']['volAvg']
        last_div = self.financials['profile']['lastDiv']
        industry = self.financials['profile']['industry']
        ceo = self.financials['profile']['ceo']
        sector = self.financials['profile']['sector']
        country = self.financials['profile']['country']
        website = self.financials['profile']['website']
        description = self.financials['profile']['description']
        full_time_employees = self.financials['profile']['fullTimeEmployees']
        address = self.financials['profile']['address']
        city = self.financials['profile']['city']
        state = self.financials['profile']['state']
        zip_code = self.financials['profile']['zip']
        phone = self.financials['profile']['phone']
        
        # Key Metrics Descriptions
        symbol_des = "The company's stock symbol."
        price_des = "The current price of the company's stock."
        beta_des = "Beta measures the sensitivity of a stock's returns to changes in the overall market."
        mkt_cap_des = "Market capitalization represents the total market value of a company's outstanding shares."
        vol_avg_des = "Average trading volume indicates the average number of shares traded per day."
        last_div_des = "The amount of the last dividend paid by the company."
        industry_des = "The industry in which the company operates."
        ceo_des = "The Chief Executive Officer of the company."
        sector_des = "The sector to which the company belongs."
        country_des = "The country where the company is headquartered."
        website_des = "The company's official website."
        description_des = "A brief description of the company and its business activities."
        full_time_employees_des = "The number of full-time employees working for the company."
        address_des = "The company's registered address."
        city_des = "The city where the company is located."
        state_des = "The state where the company is located."
        zip_code_des = "The ZIP or postal code of the company's location."
        phone_des = "The company's contact phone number."
        
        # Store metrics and their descriptions in a dictionary
        profile_metrics = {
            'symbol': [symbol, symbol_des],
            'price': [price, price_des],
            'beta': [beta, beta_des],
            'mkt_cap': [mkt_cap, mkt_cap_des],
            'vol_avg': [vol_avg, vol_avg_des],
            'last_div': [last_div, last_div_des],
            'industry': [industry, industry_des],
            'ceo': [ceo, ceo_des],
            'sector': [sector, sector_des],
            'country': [country, country_des],
            'website': [website, website_des],
            'description': [description, description_des],
            'full_time_employees': [full_time_employees, full_time_employees_des],
            'address': [address, address_des],
            'city': [city, city_des],
            'state': [state, state_des],
            'zip_code': [zip_code, zip_code_des],
            'phone': [phone, phone_des]
        }

        self.metrics['profile'] = profile_metrics

    




AAPL = Company('AAPL')
print(AAPL.news_articles)
