from nbp_api_mock.with_di.src.rate import to_pln, Currency
import httpx
from mock import patch


def mocked_get(_):
    """Replacement for httpx.get which always returns a fixed json in its body."""
    class MockedResponse:
        @staticmethod
        def json():
            return {"rates": [{"mid": 6.5}]}

        @staticmethod
        def raise_for_status():
            pass
    return MockedResponse()


def test_rate():
    with patch.object(httpx, "get", mocked_get):
        pln = to_pln(Currency.EUR, 100)
    assert pln == 650
