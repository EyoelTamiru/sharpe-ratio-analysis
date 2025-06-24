# Sharpe Ratio Analysis: AMZN and META vs S&P 500

## Project Overview
This project calculates the Sharpe ratios of Amazon (AMZN) and Meta (META) stocks, benchmarked against the S&P 500 (^GSPC), to evaluate risk-adjusted returns. It also analyzes correlations to understand how AMZN and META move with the market. The project uses Python for data fetching, analysis, and visualization, and SQL for data cleaning.

## Repository Structure
- `src/sharpe_ratio_analysis.py`: Main Python script for analysis and visualization.
- `sql/clean_data.sql`: SQL queries for data cleaning.
- `data/cleaned_stock_prices.csv`: Cleaned stock price data (generated).
- `plots/`: Visualizations (cumulative returns, rolling correlations).
- `README.md`: Project documentation.
- `.gitignore`: Excludes temporary files and database.
- `LICENSE`: MIT License.

## Setup Instructions
1. Clone the repository: `git clone <your-repo-url>`.
2. Install dependencies: `pip install yfinance pandas numpy matplotlib sqlite3`.
3. Run the script: `python src/sharpe_ratio_analysis.py`.

## Usage
- Fetches data from Yahoo Finance (2020-01-01 to 2025-06-24).
- Cleans data using SQLite, removing missing values.
- Calculates:
  - Sharpe ratios for AMZN, META, and S&P 500.
  - Correlation matrix of daily returns.
  - 30-day rolling correlations with S&P 500.
- Outputs:
  - Cleaned data: `data/cleaned_stock_prices.csv`.
  - Plots: `plots/cumulative_returns.png`, `plots/rolling_correlations.png`.
  - Console output: Sharpe ratios and correlation matrix.

## Insights
- **Sharpe Ratios**: Higher ratios indicate better risk-adjusted returns. Compare AMZN, META, and S&P 500 to assess performance.
- **Correlations**: High correlation with S&P 500 (e.g., >0.7) suggests market-driven movements; lower correlation indicates diversification potential.
- **Rolling Correlations**: Identify periods of stronger/weaker market linkage, possibly tied to company-specific or market-wide events.

## Requirements
- Python 3.8+
- Libraries: `yfinance`, `pandas`, `numpy`, `matplotlib`, `sqlite3`
- SQLite (included with Python)

## License
MIT License