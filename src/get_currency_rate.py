import requests


def get_currency_rate(currency: str) -> float:
    """
    Возвращает курс введенной валюты к рублю от бесплатного API
    :param currency: введенная валюта
    :return: курс валюты к рублю
    """
    url = f'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{currency}.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()[currency]['rub']
