def calculate_price(duration_minutes):
    """
    Calculates the price based on parking duration.
    Pricing model: 1€ per 30 minutes (0.033€ per minute)
    """
    price_per_minute = 1 / 30  # = 0.033...
    total_price = round(duration_minutes * price_per_minute, 2)
    return total_price
