import json
import requests
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, dif_currency: str, amount: str):
        base_lower = base.lower()
        dif_currency_lower = dif_currency.lower()

        if dif_currency_lower == base_lower:
            raise APIException(f'Enter different currencies.')

        try:
            base_ticker = keys[base_lower]
        except KeyError:
            raise APIException(f"It's an unknown currency {base}")
        try:
            dif_currency_ticker = keys[dif_currency_lower]
        except KeyError:
            raise APIException(f"It's an unknown currency {dif_currency}")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Failed to process amount: {amount}')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={dif_currency_ticker}')
        total_base = json.loads(r.content)[keys[dif_currency_lower]]
        total_base *= amount
        return total_base
