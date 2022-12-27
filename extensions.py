import requests
import json
from config import keys


class ConvertException(Exception):
    pass

class ValuteConverter:
    @staticmethod
    def get_price(quote: str, base: str, quantity: str):

        if base == quote:
            raise ConvertException('Конвертируемая и итоговая валюта не могут быть одинаковыми')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertException(f'Валюта {base} отсутствует в списке доступных')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertException(f'Валюта {quote} отсутствует в списке доступных')

        try:
            quantity = float(quantity)
        except ValueError:
            raise ConvertException(f'{quantity} не является числовым значением')

        headers = {
            "apikey": "KskRe2SX6FmFfiYpk1VJWQOv1QnslIWj"
        }

        response = requests.request("GET",
                                    f"https://api.apilayer.com/fixer/convert?to={quote_ticker}&from={base_ticker}&amount={quantity}",
                                    headers=headers)

        r = json.loads(response.content)
        converted = round(r['result'], 2)
        return converted