import matplotlib.pyplot as plt

def plot_budget_vs_actual(budget, actual, category):
    """
    Plot the budgeted vs actual values for a specific category.
    Truncates to the shortest length between budget and actual.
    """
    # Ensure both series have the same length
    actual_series = actual[category]
    budget_series = budget[category]
    min_len = min(len(actual_series), len(budget_series))

    months = range(1, min_len + 1)
    fig, ax = plt.subplots()
    ax.plot(months, budget_series[:min_len], label='Forecasted', marker='o')
    ax.plot(months, actual_series[:min_len], label='Actual', marker='o')
    ax.set_xlabel('Period')
    ax.set_ylabel(category)
    ax.set_title(f'{category} – Actual vs Forecast')
    ax.legend()
    return fig

def plot_forecast(forecasted_values, title):
    """
    Plot the forecasted values for a single financial metric.
    """
    months = range(1, len(forecasted_values) + 1)
    fig, ax = plt.subplots()
    ax.plot(months, forecasted_values, label='Forecasted', marker='o')
    ax.set_xlabel('Period')
    ax.set_ylabel('Amount')
    ax.set_title(f'{title} Forecast')
    ax.legend()
    return fig
