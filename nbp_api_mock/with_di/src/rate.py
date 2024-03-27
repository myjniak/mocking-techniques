from enum import StrEnum, auto

import httpx


class Currency(StrEnum):
    EUR = auto()
    USD = auto()
    CHF = auto()
    GBP = auto()


def to_pln(currency: Currency, amount: float, http_requests=httpx) -> float:
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/last"
    response = http_requests.get(url)
    response.raise_for_status()
    mid = response.json()["rates"][0]["mid"]
    return round(mid * amount, 2)
