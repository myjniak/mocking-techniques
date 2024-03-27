from src.rate import to_pln, Currency


class MockedRequests:
    def get(self, _):
        return self

    @staticmethod
    def raise_for_status():
        pass

    @staticmethod
    def json():
        return {"rates": [{"mid": 3.0}]}


def test_to_pln():
    result = to_pln(Currency.USD, 50, MockedRequests())
    assert result == 150
