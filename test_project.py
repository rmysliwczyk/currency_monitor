from project import convert_to, convert_from, get_currency_codes_from_str


def test_convert_to():
    assert convert_to(1, 10) == 0.1
    assert convert_to(1.0, 10.0) == 0.1
    assert convert_to(2, 4) == 0.5


def test_convert_from():
    assert convert_from(1, 10) == 10
    assert convert_from(1.0, 10.0) == 10
    assert convert_from(2, 4) == 8


def test_get_currency_codes_from_str():
    assert get_currency_codes_from_str("AB") == []
    assert get_currency_codes_from_str("ABC") == ["abc"]
    assert get_currency_codes_from_str("usdeur") == ["usd", "eur"]
    assert get_currency_codes_from_str("usd, eur") == ["usd", "eur"]
