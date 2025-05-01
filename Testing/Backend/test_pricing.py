from Backend.Logic.pricing import calculate_price 

def test_calculate_price_basic_cases():
    assert calculate_price(30) == 1.0
    assert calculate_price(60) == 2.0
    assert calculate_price(15) == 0.5
    assert calculate_price(0) == 0.0

def test_calculate_price_rounding():
    assert calculate_price(1) == 0.03
    assert calculate_price(2) == 0.07
    assert calculate_price(3) == 0.1

def test_calculate_price_negative():
    assert calculate_price(-30) == -1.0
