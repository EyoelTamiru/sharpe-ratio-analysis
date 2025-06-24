import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
import os

# Create directories if they don't exist
os.makedirs('data', exist_ok=True)
os.makedirs('plots', exist_ok=True)

# Step 1: Fetch data
tickers = ['AMZN', 'META', '^GSPC']
start_date = '2020-01-01'
end_date = '2025-06-24'

print("Fetching data...")
data = yf.download(tickers, start=start_date, end=end_date, progress=False)['Adj Close']
if data.empty:
    raise ValueError("No data fetched. Check internet connection or ticker symbols.")

# Step 2: Store data in SQLite
conn = sqlite3.connect('data/stock_data.db')
data.to_sql('raw_stock_prices', conn, if_exists='replace', index=True)

# Step 3: Clean data using SQL
clean_query = """
SELECT Date, AMZN, META, "^GSPC"
FROM raw_stock_prices
WHERE AMZN IS NOT NULL
  AND META IS NOT NULL
  AND "^GSPC" IS NOT NULL
  AND Date >= '2020-01-01'
  AND Date <= '2025-06-24'
ORDER BY Date;
"""
cleaned_data = pd.read_sql_query(clean_query, conn, index_col='Date', parse_dates=['Date'])
conn.close()

if cleaned_data.empty:
    raise ValueError("No data after cleaning. Check SQL query or data source.")

# Save cleaned data
cleaned_data.to_csv('data/cleaned_stock_prices.csv')

# Step 4: Calculate daily returns
returns = cleaned_data.pct_change().dropna()

# Step 5: Risk-free rate (2% annual, converted to daily)
annual_rf = 0.02
daily_rf = (1 + annual_rf)**(1/252) - 1

# Step 6: Calculate Sharpe ratios
def calculate_sharpe_ratio(returns, rf_daily):
    excess_returns = returns - rf_daily
    annualized_return = excess_returns.mean() * 252
    annualized_std = excess_returns.std() * np.sqrt(252)
    sharpe_ratio = annualized_return / annualized_std
    return sharpe_ratio

sharpe_ratios = calculate_sharpe_ratio(returns, daily_rf)
print("\nSharpe Ratios:")
for ticker, sharpe in sharpe_ratios.items():
    print(f"{ticker}: {sharpe:.4f}")

# Step 7: Correlation analysis
correlation_matrix = returns.corr()
print("\nCorrelation Matrix:")
print(correlation_matrix)

# Rolling correlation (30-day window)
rolling_corr_amzn = returns['AMZN'].rolling(window=30).corr(returns['^GSPC'])
rolling_corr_meta = returns['META'].rolling(window=30).corr(returns['^GSPC'])

# Step 8: Visualizations
# Cumulative returns
cumulative_returns = (1 + returns).cumprod()
plt.figure(figsize=(10, 6))
for col in cumulative_returns.columns:
    plt.plot(cumulative_returns.index, cumulative_returns[col], label=col)
plt.title('Cumulative Returns (2020-2025)')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.grid(True)
plt.savefig('plots/cumulative_returns.png')
plt.close()

# Rolling correlations
plt.figure(figsize=(10, 6))
plt.plot(rolling_corr_amzn.index, rolling_corr_amzn, label='AMZN vs S&P 500')
plt.plot(rolling_corr_meta.index, rolling_corr_meta, label='META vs S&P 500')
plt.title('30-Day Rolling Correlation with S&P 500')
plt.xlabel('Date')
plt.ylabel('Correlation')
plt.legend()
plt.grid(True)
plt.savefig('plots/rolling_correlations.png')
plt.close()

print("\nAnalysis complete. Check 'data/' for cleaned data and 'plots/' for visualizations.")