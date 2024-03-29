from nbp_api_mock.with_di.src.rate import to_pln, Currency
import httpx
from mock import patch


class MockedResponse:
    @staticmethod
    def json():

        return {"rates": [{"mid": 6.5}]}

    @staticmethod
    def raise_for_status():
        pass


def test_rate():
    with patch.object(httpx, "get", return_value=MockedResponse()) as mocked_get:
        pln = to_pln(Currency.EUR, 100)
    assert pln == 650
    mocked_get.assert_called_once_with("https://api.nbp.pl/api/exchangerates/rates/a/eur/last")
