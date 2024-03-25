from src.rate import to_pln, Currency


class MockedRequests:
    def get(self, *_):
        return self

    def raise_for_status(self):
        pass

    def json(self):
        return {"rates": [{"mid": 3.0}]}


def test_to_pln():
    pln = to_pln(Currency.USD, 50, MockedRequests())
    assert pln == 150
