import numpy as np
from sklearn.linear_model import LinearRegression
from config import (
    HISTORICAL_REVENUE,
    HISTORICAL_COSTS,
    HISTORICAL_OPERATING_EXPENSES,
    FORECAST_PERIOD,
)

def _linear_forecast(data, periods=FORECAST_PERIOD):
    """
    Generic linear regression forecaster.
    """
    X = np.arange(len(data)).reshape(-1, 1)
    y = np.array(data)
    model = LinearRegression()
    model.fit(X, y)
    future_X = np.arange(len(data), len(data) + periods).reshape(-1, 1)
    return model.predict(future_X).tolist()

def forecast_revenue():
    return _linear_forecast(HISTORICAL_REVENUE)

def forecast_costs():
    return _linear_forecast(HISTORICAL_COSTS)

def forecast_operating_expenses():
    return _linear_forecast(HISTORICAL_OPERATING_EXPENSES)

def forecast_net_income(forecasted_revenue, forecasted_costs, forecasted_operating_expenses):
    forecasted_net_income = [
        r - c - o for r, c, o in zip(forecasted_revenue, forecasted_costs, forecasted_operating_expenses)
    ]
    return forecasted_net_income
