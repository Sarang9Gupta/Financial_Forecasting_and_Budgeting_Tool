import streamlit as st
import pandas as pd
import yfinance as yf  # ⬅️ New import

from budget import compare_actual_vs_forecast
from forecasting import (
    forecast_revenue, forecast_costs,
    forecast_operating_expenses, forecast_net_income
)
from analysis import calculate_growth_rate, calculate_profit_margin
from visualization import plot_budget_vs_actual, plot_forecast
from config import (
    HISTORICAL_REVENUE, HISTORICAL_COSTS,
    HISTORICAL_OPERATING_EXPENSES
)

st.set_page_config(page_title="Financial Forecasting & Budgeting", layout="wide")
st.title("📊 Financial Forecasting and Budgeting Tool")

# ──────────────────────────────────────────────────────────────
# Ticker Input & Real Data Option
# ──────────────────────────────────────────────────────────────
ticker = st.text_input("Enter stock ticker (e.g. AAPL, MSFT, INFY.NS):", "AAPL")
if st.button("🔄 Load Company Financials"):
    try:
        tkr = yf.Ticker(ticker)
        df = tkr.quarterly_financials.T.fillna(0)
        revenue = df["Total Revenue"].astype(float).tolist()
        costs = df["Cost Of Revenue"].astype(float).tolist()
        opex = df["Operating Expense"].astype(float).tolist()
        net = [r - c - o for r, c, o in zip(revenue, costs, opex)]

        st.session_state["revenue"] = revenue
        st.session_state["costs"] = costs
        st.session_state["opex"] = opex
        st.session_state["net"] = net
        st.success(f"Loaded data for {ticker.upper()}")
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Use real data if available
HISTORICAL_REVENUE = st.session_state.get("revenue", HISTORICAL_REVENUE)
HISTORICAL_COSTS = st.session_state.get("costs", HISTORICAL_COSTS)
HISTORICAL_OPERATING_EXPENSES = st.session_state.get("opex", HISTORICAL_OPERATING_EXPENSES)
HISTORICAL_NET = st.session_state.get("net", [
    r - c - o for r, c, o in zip(HISTORICAL_REVENUE, HISTORICAL_COSTS, HISTORICAL_OPERATING_EXPENSES)
])

# ──────────────────────────────────────────────────────────────
# Step 1 – Historical Actuals
# ──────────────────────────────────────────────────────────────
st.header("Step 1 · Historical Actuals")
actual = {
    "Revenue": HISTORICAL_REVENUE,
    "Cost_of_Goods_Sold": HISTORICAL_COSTS,
    "Operating_Expenses": HISTORICAL_OPERATING_EXPENSES,
    "Net_Income": HISTORICAL_NET
}
actual_df = pd.DataFrame(actual, index=range(1, len(HISTORICAL_REVENUE) + 1))
with st.expander("📂 Show historical table"):
    st.dataframe(actual_df, use_container_width=True)

# ──────────────────────────────────────────────────────────────
# Step 2 – Forecasts
# ──────────────────────────────────────────────────────────────
st.header("Step 2 · Forecasts")
forecasted_revenue = forecast_revenue()
forecasted_costs = forecast_costs()
forecasted_opex = forecast_operating_expenses()
forecasted_net_income = forecast_net_income(
    forecasted_revenue, forecasted_costs, forecasted_opex
)

forecast = {
    "Revenue": forecasted_revenue,
    "Cost_of_Goods_Sold": forecasted_costs,
    "Operating_Expenses": forecasted_opex,
    "Net_Income": forecasted_net_income,
}
forecast_df = pd.DataFrame(forecast, index=range(1, len(forecasted_revenue) + 1))
with st.expander("📈 Show forecast table"):
    st.dataframe(forecast_df, use_container_width=True)

# ──────────────────────────────────────────────────────────────
# Step 3 – Actual vs Forecast Comparison
# ──────────────────────────────────────────────────────────────
st.header("Step 3 · Actual vs Forecast")
comparison = compare_actual_vs_forecast(actual, forecast)
comparison_df = pd.DataFrame(comparison, index=actual_df.index)
with st.expander("🔍 Show comparison table"):
    st.dataframe(comparison_df, use_container_width=True)

# ──────────────────────────────────────────────────────────────
# Step 4 – Key Metrics
# ──────────────────────────────────────────────────────────────
st.header("Step 4 · Key Metrics")

def last_or_zero(lst):
    return lst[-1] if lst else 0.0

rev_growth = last_or_zero(calculate_growth_rate(HISTORICAL_REVENUE))
cost_growth = last_or_zero(calculate_growth_rate(HISTORICAL_COSTS))
opex_growth = last_or_zero(calculate_growth_rate(HISTORICAL_OPERATING_EXPENSES))
profit_margin = calculate_profit_margin(
    sum(HISTORICAL_REVENUE), sum(HISTORICAL_COSTS)
)

col1, col2 = st.columns(2)
with col1:
    st.metric("📈 Revenue Growth (last period)", f"{rev_growth:.2f}%")
    st.metric("📉 Cost Growth (last period)", f"{cost_growth:.2f}%")
with col2:
    st.metric("💸 Opex Growth (last period)", f"{opex_growth:.2f}%")
    st.metric("💰 Overall Profit Margin", f"{profit_margin:.2f}%")

# ──────────────────────────────────────────────────────────────
# Step 5 – Visualisations
# ──────────────────────────────────────────────────────────────
st.header("Step 5 · Visualisations")

plot_choice = st.selectbox(
    "Select a chart:",
    (
        "Revenue – Actual vs Forecast",
        "Cost_of_Goods_Sold – Actual vs Forecast",
        "Operating_Expenses – Actual vs Forecast",
        "Revenue – Forecast trend",
        "Costs – Forecast trend",
        "Operating Expenses – Forecast trend",
        "Net Income – Forecast trend",
    ),
)

if "Actual vs" in plot_choice:
    category = plot_choice.split(" – ")[0]
    st.pyplot(plot_budget_vs_actual(actual, forecast, category))
else:
    label = plot_choice.split(" – ")[0]
    data_lookup = {
        "Revenue": forecasted_revenue,
        "Costs": forecasted_costs,
        "Operating Expenses": forecasted_opex,
        "Net Income": forecasted_net_income,
    }
    st.pyplot(plot_forecast(data_lookup[label], label))
