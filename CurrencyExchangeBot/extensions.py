import requests


class APIException(Exception):
    def __init__(self, text):  #данный метод используется для инициализации APIException который принимает текст в качестве аргумента
        self.text = text

    def __str__(self):          #используется для возврата строкового представления объекта APIException.
        return self.text        # В этом случае он просто возвращает текстовое сообщение об ошибке, которое было
                                # передано в метод __init__



class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        try:
            base = base.upper()
            quote = quote.upper()
            url = f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}'
            response = requests.get(url).json()
            price = response[quote]
            return price * amount
        except KeyError:
            raise APIException(f'Ошибка: неверное название валюты: {base} или {quote}')
