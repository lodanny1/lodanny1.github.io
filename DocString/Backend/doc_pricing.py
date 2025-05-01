def calculate_price(duration_minutes):
    """
    Calculates parking cost based on the duration in minutes.

    Pricing model:
        - €1 per 30 minutes

    Args:
        duration_minutes (int): Duration of the reservation in minutes.

    Returns:
        float: The total cost.
    """
    price_per_minute = 1 / 30  # = 0.033...
    total_price = round(duration_minutes * price_per_minute, 2)
    return total_price
