from src.rate import to_pln, Currency


def test_rate(httpx_mock):
    """Make all HTTP requests always return this json."""
    httpx_mock.add_response(json={"rates": [{"mid": 2}]})
    pln = to_pln(Currency.EUR, 100)
    assert pln == 200
