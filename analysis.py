# analysis.py
import numpy as np

def calculate_growth_rate(values):
    """
    Safely calculate the growth rate for a series of values.
    Handles division by zero and missing/short data.
    """
    growth_rate = []
    for i in range(1, len(values)):
        previous = values[i - 1]
        current = values[i]
        if previous == 0:
            growth_rate.append(0.0)  # Avoid division by zero
        else:
            growth = ((current - previous) / previous) * 100
            growth_rate.append(growth)
    return growth_rate


def calculate_profit_margin(revenue, costs):
    """
    Calculate profit margin safely.
    """
    if revenue == 0:
        return 0.0
    return ((revenue - costs) / revenue) * 100
