import yfinance as yf
import pandas as pd

def get_real_data(ticker_symbol, use_ttm=False):
    ticker = yf.Ticker(ticker_symbol)

    # Get annual + quarterly financials
    annual_df = ticker.financials.T
    quarterly_df = ticker.quarterly_financials.T

    # Combine and sort chronologically
    full_df = pd.concat([annual_df, quarterly_df])
    full_df = full_df.sort_index()

    # Drop rows where any field is missing
    df = full_df[["Total Revenue", "Cost Of Revenue", "Operating Expense"]].dropna()

    # Convert to numeric
    df = df.astype(float)

    # Optional: Convert to Trailing 12 Months (TTM) rolling sum
    if use_ttm and len(df) >= 4:
        df = df.rolling(window=4).sum().dropna()

    revenue = df["Total Revenue"].tolist()
    costs = df["Cost Of Revenue"].tolist()
    opex = df["Operating Expense"].tolist()
    net_income = [r - c - o for r, c, o in zip(revenue, costs, opex)]

    return revenue, costs, opex, net_income



# Set this once at app start
TICKER = "AAPL"  # Change this dynamically via Streamlit dropdown if desired
HISTORICAL_REVENUE, HISTORICAL_COSTS, HISTORICAL_OPERATING_EXPENSES, NET_INCOME = get_real_data(TICKER, use_ttm=True)

BUDGET = {
    'Revenue': HISTORICAL_REVENUE,
    'Cost_of_Goods_Sold': HISTORICAL_COSTS,
    'Operating_Expenses': HISTORICAL_OPERATING_EXPENSES,
    'Net_Income': NET_INCOME
}

FORECAST_PERIOD = len(HISTORICAL_REVENUE)
